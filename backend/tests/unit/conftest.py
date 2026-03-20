from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).resolve().parents[1] / "../.env.test"
load_dotenv(dotenv_path=env_path)

import pytest
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.crud.vectors import get_vector_neighbors
from app.schemas.vectors import VectorSearchResponse, VectorSearchItem
from app.utils.assistant import (
    get_api_embedding,
    get_llm_api_response
)
from app.utils.documents import get_txt_document_embed_data_from_api
from supabase import create_client

from io import BytesIO
import os

API_PREFIX = "/api/v1"

NONEXISTENT_BOT_ID = 99999
NONEXISTENT_DOC_ID = 99999
NONEXISTENT_FB_ID = 99999
TEST_TXT_SIZE = 72

SAMPLE_EMBEDDING = [0.1] * 768

TEST_USER_EMAIL = "test@example.com"
TEST_USER_PASSWORD = "test_password_123"


@asynccontextmanager
async def test_lifespan(app):
    yield




@pytest.fixture
def app():
    test_app = FastAPI(title="Mock CustomChat API", version="1.0.0", lifespan=test_lifespan)

    test_app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    test_app.include_router(api_router, prefix="/api/v1")

    test_app.dependency_overrides[get_api_embedding] = lambda: MockServices()
    test_app.dependency_overrides[get_llm_api_response] = lambda: MockServices()
    test_app.dependency_overrides[get_vector_neighbors] = lambda: MockServices()
    test_app.dependency_overrides[get_txt_document_embed_data_from_api] = lambda: MockServices()

    return test_app


@pytest.fixture
def client(app, mocker):
    """
    Creates test client which allows requests to the endpoints without starting a server
    """
    mocker.patch(
        "app.api.v1.endpoints.assistant.get_api_embedding",
        return_value=SAMPLE_EMBEDDING
    )
    mocker.patch(
        "app.api.v1.endpoints.assistant.get_llm_api_response",
        return_value="Test llm assistant response!"
    )
    mocker.patch(
        "app.api.v1.endpoints.assistant.get_vector_neighbors",
        return_value=VectorSearchResponse(
                neighbors=[
                    VectorSearchItem(vec_id=1, context="Context number one."),
                    VectorSearchItem(vec_id=2, context="Context number two."),
                    VectorSearchItem(vec_id=3, context="Context number three."),
                    VectorSearchItem(vec_id=4, context="Context number four."),
                    VectorSearchItem(vec_id=5, context="Context number five.")
                ]
        )
    )
    mocker.patch(
        "app.api.v1.endpoints.documents.get_document_embed_data_from_api",
        return_value={
            "embedding_objects": [
                {"chunk": "This is chunk one.", "embedding": SAMPLE_EMBEDDING},
                {"chunk": "This is chunk two.", "embedding": SAMPLE_EMBEDDING}
            ]
        }
    )

    with TestClient(app) as client:
        yield client


# Authentication Fixtures


@pytest.fixture(scope="session", autouse=True)
def ensure_test_user_exists():
    """
    Ensure test user exists before running any tests.
    """
    url = os.getenv("SUPABASE_URL")
    service_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

    if not service_key:
        pytest.skip("SUPABASE_SERVICE_ROLE_KEY not set - cannot create test user")

    supabase = create_client(url, service_key)

    try:
        supabase.auth.admin.create_user({
            "email": TEST_USER_EMAIL,
            "password": TEST_USER_PASSWORD,
            "email_confirm": True,
            "user_metadata": {
                "first_name": "John",
                "last_name": "Doe",
                "company":  "DoubleOSeven",
                "phone": "1234567890"
            }
        })
        print(f"Created test user: {TEST_USER_EMAIL}")
    except Exception as e:
        if "already" in str(e).lower():
            print(f"Test user already exists: {TEST_USER_EMAIL}")
        else:
            print(f"Could not create test user: {e}")


@pytest.fixture(scope="session")
def supabase_test_client():
    """Create Supabase client for tests."""
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_ANON_KEY")
    return create_client(url, key)


@pytest.fixture(scope="session")
def auth_token(supabase_test_client):
    """
    Get auth token for test user.

    Signs in as the test user and returns the JWT token.
    """
    try:
        response = supabase_test_client.auth.sign_in_with_password({
            "email": TEST_USER_EMAIL,
            "password": TEST_USER_PASSWORD
        })
        return response.session.access_token
    except Exception as e:
        pytest.fail(
            f"Failed to authenticate test user.\n"
            f"Make sure test user exists: {TEST_USER_EMAIL}\n"
            f"Error: {e}"
        )


@pytest.fixture
def auth_headers(auth_token):
    """Provide authentication headers for test requests."""
    return {"Authorization": f"Bearer {auth_token}"}


@pytest.fixture
def invalid_auth_headers():
    """Provides invalid authentication headers for testing auth failures."""
    return {"Authorization": "Bearer invalid_token"}


@pytest.fixture
def test_user_id(supabase_test_client, auth_token):
    """Get the test user's ID."""
    user = supabase_test_client.auth.get_user(auth_token)
    return user.user.id

# Sample File Fixtures


@pytest.fixture
def sample_txt_file():
    """Returns a BytesIO object that can be used as a file upload as a sample text file for upload tests."""
    content = b"This is a test document.\nIt has multiple lines.\nFor testing purposes."
    return BytesIO(content)


# do sample pdf


# do sample docx


@pytest.fixture
def large_file():
    """
    Provides a file that exceeds the size limit (>10MB).

    Used for testing file size validation.
    """
    size = 11 * 1024 * 1024  # 11MB
    content = b"x" * size
    return BytesIO(content)


@pytest.fixture
def invalid_file_exe():
    """
    Provides an executable file for testing file type rejection.

    EXE files should be rejected by the API.
    """
    # MZ signature for Windows executables
    content = b"MZ\x90\x00\x03"
    return BytesIO(content)


# Test Data Fixtures


@pytest.fixture
def sample_document_data():
    """Provide sample document metadata for creation."""
    return {
        "doc_name": "test_document",
    }


@pytest.fixture
def sample_bot_data():
    """Provides sample bot data for creation."""
    return {
        "bot_name": "Test Bot",
        "bot_desc": "A bot for testing",
        "avatar": "base",
        "color": "tan",
        "storage": 0,
        "uses": 0
    }


@pytest.fixture
def sample_feedback_data():
    """Provides sample feedback data for creation."""
    return {
        "fb_date": "2026-01-06",
        "fb_time": "10:30:15",
        "fb_desc": "Sample feedback data!",
        "is_neg": True,
        "use_log": None
    }


@pytest.fixture
def sample_assistant_request():
    """Provides sample assistant request for llm response, need to add ["bot_api_key"]"""
    return {
        "chat_history": [
            {
                "role": "USER",
                "message": "Is this a test question?"
            },
            {
                "role": "ASSISTANT",
                "message": "Yes it is a test question?"
            }
        ],
        "user_input": "What is an llm bot response?"
    }


# Database/Resource Fixtures (with cleanup)


@pytest.fixture
def created_bot(client, auth_headers, sample_bot_data):
    """Creates a test bot and return its values."""
    response = client.post(f"{API_PREFIX}/bots", json=sample_bot_data, headers=auth_headers)
    bot = response.json()

    yield bot

    client.delete(f"{API_PREFIX}/bots/{bot["bot_info"]["bot_id"]}", headers=auth_headers)


@pytest.fixture
def created_document(client, auth_headers, created_bot, sample_txt_file):
    """Creates a test document and returns its data. Cleans up after test."""
    files = {"file": ("fixture_test.txt", sample_txt_file, "text/plain")}
    data = {
        "doc_name": "fixture_test",
    }

    response = client.post(
        f"{API_PREFIX}/bots/{created_bot["bot_info"]["bot_id"]}/documents",
        files=files,
        data=data,
        headers=auth_headers
    )
    document = response.json()

    yield document

    try:
        client.delete(
            f"{API_PREFIX}/bots/{created_bot["bot_info"]["bot_id"]}/documents/{document['doc_id']}",
            headers=auth_headers
        )
    except Exception:
        pass  # Document might already be deleted by the test


# Utility Fixtures

@pytest.fixture(scope="session")
def test_config():
    """
    Provides test-specific configuration.

    Usage:
        def test_something(test_config):
            base_url = test_config["base_url"]
    """
    return {
        "base_url": "http://testserver",
        "timeout": 30,
        "max_file_size": 10 * 1024 * 1024,  # 10MB
        "allowed_file_types": ["application/pdf", "text/plain"],
    }
