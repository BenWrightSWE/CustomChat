import pytest
from fastapi.testclient import TestClient
from io import BytesIO
from backend.app.main import app
import os
from supabase import create_client
from datetime import time, date


NONEXISTENT_BOT_ID = 99999
NONEXISTENT_DOC_ID = 99999
TEST_TXT_SIZE = 72

TEST_USER_EMAIL = "test@example.com"
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
            "email_confirm": True
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
def auth_token(supabase_client):
    """
    Get auth token for test user.

    Signs in as the test user and returns the JWT token.
    """
    try:
        response = supabase_client.auth.sign_in_with_password({
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
    """
    Provides invalid authentication headers for testing auth failures.

    Usage:
        def test_unauthorized(client, invalid_auth_headers):
            response = client.get("/protected", headers=invalid_auth_headers)
            assert response.status_code == 401
    """
    return {"Authorization": "Bearer invalid_token"}


@pytest.fixture
def test_user_id(supabase_client, auth_token):
    """Get the test user's ID."""
    user = supabase_client.auth.get_user(auth_token)
    return user.user.id

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
    """
    Provide sample document metadata for creation.

    Usage:
        def test_create(client, auth_headers, sample_txt_file, sample_document_data):
            files = {"file": ("test.txt", sample_txt_file, "text/plain")}
            response = client.post("/documents", files=files, data=sample_document_data)
    """
    return {
        "doc_name": "test_document",
        "doc_type": ".txt",
        "doc_size": 9
    }


@pytest.fixture
def sample_bot_data():
    """
    Provides sample bot data for creation.

    Adjust fields based on your BotCreate schema.
    """
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
    """
    Provides sample feedback data for creation.

    Adjust fields based on your FeedbackCreate schema.
    """
    return {
        "fb_date": date(2026, 1, 6),
        "fb_time": time(10, 30, 15),
        "is_neg": True,
        "fb_desc": "Sample feedback data!",
        "use_log": None
    }


# Database/Resource Fixtures (with cleanup)


@pytest.fixture
def test_bot_id(client, auth_headers, sample_bot_data):
    """
    Creates a test bot and return its ID. Cleans up after test.

    Usage:
        def test_something(client, auth_headers, test_bot_id):
            response = client.get(f"/bots/{test_bot_id}")
    """
    # Create bot
    response = client.post("/bots", json=sample_bot_data, headers=auth_headers)
    bot = response.json()
    bot_id = bot["bot_id"]

    yield bot_id  # Provide to test

    # Cleanup: Delete bot after test
    client.delete(f"/bots/{bot_id}", headers=auth_headers)


@pytest.fixture
def created_document(client, auth_headers, test_bot_id, sample_txt_file):
    """
    Creates a test document and return its data. Cleans up after test.

    Usage:
        def test_get_document(client, auth_headers, created_document):
            doc_id = created_document["doc_id"]
            response = client.get(f"/bots/1/documents/{doc_id}")
    """
    # Create document
    files = {"file": ("fixture_test.txt", sample_txt_file, "text/plain")}
    data = {
        "doc_name": "fixture_test",
        "doc_type": ".txt",
        "doc_size": 50
    }

    response = client.post(
        f"/bots/{test_bot_id}/documents",
        files=files,
        data=data,
        headers=auth_headers
    )
    document = response.json()

    yield document  # Provide to test

    # Cleanup: Delete document after test
    try:
        client.delete(
            f"/bots/{test_bot_id}/documents/{document['doc_id']}",
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
