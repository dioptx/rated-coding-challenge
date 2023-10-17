import pytest
import app

client = TestClient(app)

def test_get_transaction():
    response = client.get("/transactions/sample_hash")  # replace 'sample_hash' with a hash that actually exists in your DB for a meaningful test
    assert response.status_code == 200
    assert "hash" in response.json()

def test_get_transaction_not_found():
    response = client.get("/transactions/nonexistent_hash")
    assert response.status_code == 404

def test_get_stats():
    response = client.get("/stats")
    assert response.status_code == 200
    assert "total_transactions_in_db" in response.json()
