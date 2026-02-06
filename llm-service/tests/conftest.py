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
    Returns a string that can be used as user input for the llm.
    """
    return "Where are the TestCorps main offices located at?"


@pytest.fixture
def sample_context():
    """
    Returns a string which holds the context for the users question.
    """
    return ["Computer"]


def sample_history():
    """
    Returns a string including the previous chat history.
    """
    return ""


@pytest.fixture
def test_api_key():
    return {"X-API-KEY": os.getenv("EMBEDDING_API_KEY")}