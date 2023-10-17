# Ethereum Transactions Analysis Project

## Overview
This project aims to manipulate and analyze an Ethereum transaction dataset using Python and FastAPI. The solution focuses on calculating the execution timestamp of each transaction, computing the gas cost, fetching the approximate price of ETH at the transaction execution time, and computing the dollar cost of gas used. Additionally, the processed transactions are populated into a PostgreSQL database.

## Project Structure
- `fastapi-app/`: Contains the FastAPI code for serving transaction data and stats.
- `docker-compose.yml`: Docker Compose file for orchestrating the Postgres and FastAPI server containers.
- `ethereum_txs.csv`: The Ethereum transaction dataset.
- `notebooks/`: Contains Jupyter Notebook(s) for data processing and analysis.
- `tests/`: Contains test files for the FastAPI application.

## Setup and Execution

### Prerequisites
- Docker and Docker Compose installed on your machine.

### Steps
1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Build and start the Docker containers using Docker Compose:
   ```bash
   docker-compose up --build -d

## Key Questions
1. What is the method to compute the approximate execution timestamp for each transaction?
2. How do we calculate the gas cost for each transaction, expressed in Gwei?
3. How can we fetch the real-time approximate price of ETH at the time of transaction execution?
4. What are the steps to populate the processed transactions into a local PostgreSQL database?
5. How is the FASTAPI implemented to serve both individual transaction data and global statistics?

## Setup and Execution

### Prerequisites
- Docker must be installed.

### Steps
1. **Clone the Repository**: Clone the project repository to your local system.
2. **Navigate to Project Directory**: Move to the project's root directory in your terminal.
3. **Run Docker Compose**: Execute the following command to build and start the Docker containers.
    ```bash
    docker-compose up --build -d
    ```
4. **Access Jupyter Notebook**: Open `http://localhost:8888` in a web browser. Use the password `password` to log in and run the data processing notebooks.
5. **FASTAPI**: The API will be live at `http://localhost:5001`. Use the following endpoints:
    - Fetch a transaction: `GET /transactions/:hash`
    - Retrieve global stats: `GET /stats`
6. **Shutdown**: To halt and remove the Docker containers, use:
    ```bash
    docker-compose down
    ```

## API Endpoints
- **Fetch Transaction**
  - **URL**: `/transactions/:hash`
  - **Method**: `GET`
  - **URL Params**: `hash=[string]`
  - **Success**: `200 OK`
  - **Failure**: `404 Not Found`

- **Global Stats**
  - **URL**: `/stats`
  - **Method**: `GET`
  - **Success**: `200 OK`

## Database Schema
The PostgreSQL database, named `transactions_db`, includes a `transactions` table containing the processed transaction data.

## Notebooks
Jupyter Notebooks in the `notebooks/` directory contain all the code required for data processing and database population.

## Conclusion
This project not only manipulates and analyzes Ethereum transaction data but also demonstrates the capability of building robust APIs for blockchain data dissemination.