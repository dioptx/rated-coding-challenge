from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
from datetime import datetime

app = FastAPI()

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

# Initialize DB connection
conn = psycopg2.connect(
    dbname='transactions_db',
    user='user',
    password='password',
    host='postgres'
) # Todo: This is bad practice, ideally this would be done in a separate interface that uses a centrally managed secret and imported here



class Transaction(BaseModel):
    hash: str
    from_address: str
    to_address: str
    block_number: int
    executed_at: datetime
    gas_used: int
    gas_cost_in_dollars: float

    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S')
        }
class Stats(BaseModel):
    total_transactions_in_db: int
    total_gas_used: int
    total_gas_cost_in_dollars: float

@app.get("/transactions/{tx_hash}", response_model=Transaction)
async def get_transaction(tx_hash: str):
    # Create table if it doesn't exist
    create_table_if_not_exists()
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT
                hash, from_address, to_address, block_number,
                executed_at, gas_used, gas_cost_in_dollars
            FROM transactions
            WHERE hash = %s;
        """, (tx_hash,))
        result = cursor.fetchone()
        if result is None:
            raise HTTPException(status_code=404, detail="Transaction not found")
        columns = [desc[0] for desc in cursor.description]
        transaction = dict(zip(columns, result))
    return transaction

from fastapi import HTTPException

@app.get("/stats", response_model=Stats)
async def get_stats():
    # Create table if it doesn't exist
    create_table_if_not_exists()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT
                    COUNT(*) AS total_transactions_in_db,
                    SUM(gas_used) AS total_gas_used,
                    SUM(gas_cost_in_dollars) AS total_gas_cost_in_dollars
                FROM transactions;
            """)
            result = cursor.fetchone()
            if result is None:
                raise HTTPException(status_code=500, detail="No data found in the database")

            columns = [desc[0] for desc in cursor.description]
            stats = dict(zip(columns, result))

            if 'total_gas_used' not in stats:
                stats = {'total_transactions_in_db': 0, 'total_gas_used': 0, 'total_gas_cost_in_dollars': 0}

        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve stats")
