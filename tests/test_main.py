# калямаля
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200

def test_upload_image_no_file():
    response = client.post("/ocr/upload", files={})
    assert response.status_code == 400
