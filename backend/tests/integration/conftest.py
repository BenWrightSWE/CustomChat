from dotenv import load_dotenv
from pathlib import Path
import uuid


env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=env_path)

import pytest
from fastapi.testclient import TestClient

from app.main import app
from supabase import create_client

from io import BytesIO
import os

API_PREFIX = "/api/v1"

TEST_TXT_SIZE = 72

TEST_USER_PASSWORD = "test_password_123"


@pytest.fixture
def client():
    """
    Creates test client which allows requests to the endpoints without starting a server

    Usage:
        def test_something(client):
            response = client.get("/endpoint")
    """
    return TestClient(app)


# Authentication Fixtures


@pytest.fixture
def create_test_user():
    url = os.getenv("SUPABASE_URL")
    service_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

    supabase = create_client(url, service_key)

    email = f"test_{uuid.uuid4()}@example.com"
    password = "testpassword123"

    response = supabase.auth.admin.create_user({
        "email": email,
        "password": password,
        "email_confirm": True,
        "user_metadata": {
            "first_name": "John",
            "last_name": "Doe"
        }
    })

    user_id = response.user.id

    yield {
        "email": email,
        "password": password,
        "user_id": user_id
    }

    supabase.auth.admin.delete_user(user_id)


@pytest.fixture
def supabase_test_client():
    """Create Supabase client for tests."""
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_ANON_KEY")
    return create_client(url, key)


@pytest.fixture
def auth_token(create_test_user, supabase_test_client):

    response = supabase_test_client.auth.sign_in_with_password({
        "email": create_test_user["email"],
        "password": create_test_user["password"]
    })

    return response.session.access_token


# This is called by the test, creates the user, logs them in, gets the auth token, and provides the auth headers.
@pytest.fixture
def auth_headers(auth_token):
    """Provide authentication headers for test requests."""
    return {"Authorization": f"Bearer {auth_token}"}


# CREATION FIXTURES


@pytest.fixture
def sample_bot_data():
    """
    Provides sample bot data for creation.
    """
    return {
        "bot_name": "Test Bot",
        "bot_desc": "A bot for testing",
        "avatar": "base",
        "color": "tan",
        "storage": 0,
        "uses": 0
    }




# Sample File Fixtures

@pytest.fixture
def sample_txt_file():
    """
    Returns a BytesIO object that can be used as a file upload as a sample text file for upload tests.

    Usage:
        def test_upload(client, auth_headers, sample_txt_file):
            files = {"file": ("test.txt", sample_txt_file, "text/plain")}
            response = client.post("/upload", files=files, headers=auth_headers)
    """
    content = b"This is a test document.\nIt has multiple lines.\nFor testing purposes."
    return BytesIO(content)


# do sample pdf


# do sample docx

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
def sample_assistant_request():
    """
    Provides sample assistant request for llm response.
    """
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
    """
    Creates a test bot and return its ID. Cleans up after test.

    Usage:
        def test_something(client, auth_headers, test_bot_id):
            response = client.get(f"/bots/{test_bot_id}")
    """
    response = client.post(f"{API_PREFIX}/bots", json=sample_bot_data, headers=auth_headers)
    bot = response.json()

    yield bot

    client.delete(f"{API_PREFIX}/bots/{bot["bot_id"]}", headers=auth_headers)


@pytest.fixture
def created_document(client, auth_headers, created_bot, sample_txt_file):
    """
    Creates a test document and return its data. Cleans up after test.

    Usage:
        def test_get_document(client, auth_headers, created_document):
            doc_id = created_document["doc_id"]
            response = client.get(f"/bots/1/documents/{doc_id}")
    """
    files = {"file": ("fixture_test.txt", sample_txt_file, "text/plain")}
    data = {
        "doc_name": "fixture_test",
        "doc_type": ".txt",
        "doc_size": 50
    }

    response = client.post(
        f"{API_PREFIX}/bots/{created_bot["bot_id"]}/documents",
        files=files,
        data=data,
        headers=auth_headers
    )
    document = response.json()

    yield document

    try:
        client.delete(
            f"{API_PREFIX}/bots/{created_bot["bot_id"]}/documents/{document['doc_id']}",
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
