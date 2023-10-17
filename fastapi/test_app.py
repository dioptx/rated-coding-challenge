import pytest
import app

client = TestClient(app)

def test_get_transaction():
    response = client.get("/transactions/0xc055b65e39c15e1bc90cb4ccb2daac6b59c02ec1aa6c4216276054b4f31ed90a")
    assert response.status_code == 200
    assert "hash" in response.json()

def test_get_transaction_not_found():
    response = client.get("/transactions/nonexistent_hash")
    assert response.status_code == 404

def test_get_stats():
    response = client.get("/stats")
    assert response.status_code == 200
    assert "total_transactions_in_db" in response.json()
