from kafka import KafkaConsumer
import json
import pandas as pd
from datetime import timedelta
import psycopg2
import requests
from time import sleep
from tqdm import tqdm

# Initialize DB connection
conn = psycopg2.connect(
    dbname='transactions_db',
    user='user',
    password='password',
    host='postgres'
)

def get_eth_price(timestamp):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd&at={timestamp}"
    retry_count = 0
    max_retries = 5
    sleep_time = 5  # initial sleep time in seds

    while retry_count < max_retries:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()['ethereum']['usd']
        elif response.status_code == 429:
            sleep(sleep_time)
            sleep_time *= 2  # Exponential backoff
            sleep_time = min(sleep_time, 60)  # Cap the sleep time at 60 seconds
            retry_count += 1
        else:
            print(f"Failed to retrieve data: {response.status_code}")
            return None
    print(f"Failed to retrieve data after {max_retries} retries")
    return None

def create_table_if_not_exists():
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS transactions (
        id SERIAL PRIMARY KEY,
        hash TEXT NOT NULL,
        from_address TEXT NOT NULL,
        to_address TEXT NOT NULL,
        block_number INTEGER NOT NULL,
        executed_at TIMESTAMP NOT NULL,
        gas_used BIGINT NOT NULL,
        gas_cost_in_dollars DOUBLE PRECISION NOT NULL
    );
    '''
    with conn.cursor() as cursor:
        cursor.execute(create_table_query)
    conn.commit()

def insert_into_db(df):
    
    # Create table if it doesn't exist
    create_table_if_not_exists()

    with conn.cursor() as cursor:
        for _, row in df.iterrows():
            try:
                cursor.execute("""
                    INSERT INTO transactions (hash, from_address, to_address, block_number, executed_at, gas_used, gas_cost_in_dollars)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (row['hash'], row['from_address'], row['to_address'], row['block_number'], row['execution_timestamp'], row['gas'], row['gas_cost_usd']))
            except Exception as e:
                print(f"Failed to insert record: {e}")
        conn.commit()

def process_csv_line(line):
    df_line = pd.DataFrame([line])
    block_length = 12  # seconds
    df_line['block_timestamp'] = pd.to_datetime(df_line['block_timestamp'])
    df_line['execution_timestamp'] = df_line['block_timestamp'] + \
        (df_line['transaction_index'].astype(int) * timedelta(seconds=block_length / len(df_line)))
    df_line['gas_cost'] = df_line['gas'].astype(int) * df_line['gas_price'].astype(int) * 1e-9  # Gwei to ETH
    timestamp_str = df_line['execution_timestamp'].dt.strftime('%s').iloc[0]
    eth_price_usd = get_eth_price(timestamp_str)
    df_line['eth_price_usd'] = eth_price_usd
    df_line['gas_cost_usd'] = df_line['gas_cost'] * df_line['eth_price_usd']
    insert_into_db(df_line)

# Initialize Kafka Consumer
consumer = KafkaConsumer(
    'eth_txs_topic',
    bootstrap_servers='kafka:9092',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# Consume messages from Kafka
for message in consumer:
    print(message.value)
    line = message.value
    process_csv_line(line)
