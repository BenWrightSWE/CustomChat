from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).resolve().parents[1] / "../.env.test"
load_dotenv(dotenv_path=env_path)

import pytest
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.testclient import TestClient
from fastapi.middleware.cors import CORSMiddleware
from app.core.llm_client import get_llm
from app.api.v1.router import api_router
from app.api.deps import get_api_key
import os


API_PREFIX = "/api/v1"


class MockLLM:
    def get_llm_response(self, *args, **kwargs):
        return "Mocked response"


@asynccontextmanager
async def test_lifespan(app):
    yield


@pytest.fixture
def app():
    test_app = FastAPI(title="LLM API", version="1.0.0", lifespan=test_lifespan)

    test_app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    test_app.include_router(
        api_router,
        prefix="/api/v1",
        tags=["llm"],
        dependencies=[Depends(get_api_key)]
    )

    test_app.dependency_overrides[get_llm] = lambda: MockLLM()

    return test_app


@pytest.fixture
def client(app):
    """
    Creates test client which allows requests to the endpoints without starting a server

    Usage:
        def test_something(client):
            response = client.get("/endpoint")
    """
    with TestClient(app) as client:
        yield client

@pytest.fixture
def mock_llm():
    #@asynccontextmanager
    #async def mock_lifespan(app: FastAPI):
    #    yield

    #app.router.lifespan_context = mock_lifespan

    app.dependency_overrides[get_llm] = lambda: MockLLM()
    yield
    app.dependency_overrides.clear()


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
        {"role": "ASSISTANT", "message": "Hello, I am TestCorp\'s chat assistant, Tester. I am here to answer any "
                                         "questions you have regarding our company to the best of my ability. "
                                         "What can I do for you today?"},
        {"role": "USER", "message": "Hello Tester, I was wondering what time you guys are generally open?"},
        {"role": "ASSISTANT", "message": "Sure! TestCorp is generally open from 5:00am to 7:00pm."}
    ]


@pytest.fixture
def test_api_key():
    return {"X-API-KEY": os.getenv("LLM_API_KEY")}