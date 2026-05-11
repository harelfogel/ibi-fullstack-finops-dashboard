"""Integration test for the upload endpoint."""

import io

from fastapi.testclient import TestClient

from tests.factories import SAMPLE_CSV_CONTENT


class TestUploadEndpoint:
    def test_upload_csv_success(self, client: TestClient):
        """Uploading a valid CSV processes all rows."""
        response = client.post(
            "/api/v1/transactions/upload",
            files={"file": ("transactions.csv", io.BytesIO(SAMPLE_CSV_CONTENT), "text/csv")},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["total_rows"] == 6
        assert data["data"]["valid_rows"] == 6
        assert data["data"]["error_rows"] == 0
        assert set(data["data"]["affected_clients"]) == {"C001", "C002", "C003"}

    def test_upload_duplicate_rejected(self, client: TestClient):
        """Uploading the same file twice rejects duplicate transaction IDs."""
        # First upload
        client.post(
            "/api/v1/transactions/upload",
            files={"file": ("tx.csv", io.BytesIO(SAMPLE_CSV_CONTENT), "text/csv")},
        )

        # Second upload (same data)
        response = client.post(
            "/api/v1/transactions/upload",
            files={"file": ("tx.csv", io.BytesIO(SAMPLE_CSV_CONTENT), "text/csv")},
        )

        data = response.json()
        assert data["success"] is True
        assert data["data"]["valid_rows"] == 0
        assert data["data"]["error_rows"] == 6

    def test_upload_invalid_format(self, client: TestClient):
        """Uploading a non-CSV file returns an error."""
        response = client.post(
            "/api/v1/transactions/upload",
            files={"file": ("data.txt", io.BytesIO(b"hello"), "text/plain")},
        )

        assert response.status_code == 400
        data = response.json()
        assert data["success"] is False

    def test_clients_after_upload(self, client: TestClient):
        """After upload, clients endpoint returns created clients."""
        client.post(
            "/api/v1/transactions/upload",
            files={"file": ("tx.csv", io.BytesIO(SAMPLE_CSV_CONTENT), "text/csv")},
        )

        response = client.get("/api/v1/clients")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        client_ids = [c["client_id"] for c in data["data"]]
        assert "C001" in client_ids
        assert "C002" in client_ids
        assert "C003" in client_ids

    def test_portfolio_after_upload(self, client: TestClient):
        """After upload, portfolio endpoint returns FIFO-calculated positions."""
        client.post(
            "/api/v1/transactions/upload",
            files={"file": ("tx.csv", io.BytesIO(SAMPLE_CSV_CONTENT), "text/csv")},
        )

        response = client.get("/api/v1/clients/C001/portfolio")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

        portfolio = data["data"]
        assert portfolio["client_id"] == "C001"
        assert len(portfolio["positions"]) == 2  # US1234567890, US9999999999

    def test_health_endpoint(self, client: TestClient):
        """Health endpoint returns healthy status."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
