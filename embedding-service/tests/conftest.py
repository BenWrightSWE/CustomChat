from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).resolve().parents[1] / ".env.test"
load_dotenv(dotenv_path=env_path)

import pytest
from fastapi.testclient import TestClient
from app.main import app
import os

API_PREFIX = "/api/v1"

@pytest.fixture
def client():
    """
    Creates test client which allows requests to the endpoints without starting a server

    Usage:
        def test_something(client):
            response = client.get("/endpoint")
    """
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def sample_user_input():
    """
    Returns a string that can be used for user input embedding tests.

    Usage:
        def test_txt_chunking(client, auth_headers, sample_txt_file):
            files = {"file": ("test.txt", sample_txt_file, "text/plain")}
            response = client.post("/embed/txt", files=files, headers=auth_headers)
    """
    return "What is a test user input?"


@pytest.fixture
def sample_txt_file():
    """
    Returns a string that can be used for txt document embedding tests.

    Usage:
        def test_txt_embed(client, auth_headers, sample_txt_file):
            files = {"file": ("test.txt", sample_txt_file, "text/plain")}
            response = client.post("/embed/txt", files=files, headers=auth_headers)
    """
    return "This is a test document.\nIt has multiple lines.\nFor testing purposes."


@pytest.fixture
def sample_large_txt_file():
    """
    Returns a string exceeding 10mb that can be used for txt document embedding tests.

    Usage:
        def test_txt_embed(client, auth_headers, sample_txt_file):
            files = {"file": ("test.txt", sample_txt_file, "text/plain")}
            response = client.post("/embed/txt", files=files, headers=auth_headers)
    """
    return "t" * (11 * 1024 * 1024)


@pytest.fixture
def test_api_key():
    """
        Returns the API key that allows use of the API.
    """
    return {"X-API-KEY": os.getenv("EMBEDDING_API_KEY")}