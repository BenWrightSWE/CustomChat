from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).resolve().parents[1] / "../.env.test"
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
    with TestClient(app) as client:
        yield client


@pytest.fixture
def sample_user_input():
    """
    Returns a string that can be used as user input for the llm.
    """
    return "Where are the TestCorps offices located at?"


@pytest.fixture
def sample_context():
    """
    Returns a string array which holds the context for the users question.
    """
    return ["TestCorp\'s headquarters is located in Atlanta, Georgia, near the Georgia Aquarium.",
            "TestCorp\'s testing facility is located in Duluth, Georgia, near the HMart.",
            "TestCorp\'s satellite office is in Chicago, Illinois near the lake."]


@pytest.fixture
def sample_history():
    """
    Returns a string including the previous chat history.
    """
    return [
        {"role": "ASSISTANT", "message": "Hello, I am TestCorp\'s chat assistant, Tester. I am here to answer any " +
                                         "questions you have regarding our company to the best of my ability. " +
                                         "What can I do for you today?"},
        {"role": "USER", "message": "Hello Tester, I was wondering what time you guys are generally open?"},
        {"role": "ASSISTANT", "message": "Sure! TestCorp is generally open from 5:00am to 7:00pm."}
    ]


@pytest.fixture
def test_api_key():
    return {"X-API-KEY": os.getenv("LLM_API_KEY")}