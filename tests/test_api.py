import pytest
from fastapi.testclient import TestClient
from app.main import app
import io
import pandas as pd

client = TestClient(app)

@pytest.fixture
def sample_excel_file():
    # Create a sample Excel file in memory
    df = pd.DataFrame({
        'mobile': ['1234567890', '9876543210']
    })
    excel_buffer = io.BytesIO()
    df.to_excel(excel_buffer, index=False)
    excel_buffer.seek(0)
    return excel_buffer

def test_upload_excel(sample_excel_file):
    response = client.post(
        "/upload-excel/",
        files={"file": ("test.xlsx", sample_excel_file, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    assert data["total_records"] == 2

def test_get_all_phones():
    response = client.get("/phones/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_specific_phone():
    response = client.get("/phones/1234567890")
    assert response.status_code == 200
    assert response.json()["mobile"] == "1234567890"

def test_update_phone():
    response = client.put(
        "/phones/1234567890",
        json={"mobile": "1111111111"}
    )
    assert response.status_code == 200
    assert response.json()["mobile"] == "1111111111"

def test_delete_phone():
    response = client.delete("/phones/9876543210")
    assert response.status_code == 200
    assert response.json()["message"] == "Phone number deleted successfully"