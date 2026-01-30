from tests.conftest import (
    NONEXISTENT_BOT_ID,
    NONEXISTENT_DOC_ID,
    TEST_TXT_SIZE,
    API_PREFIX
)


class TestCreateDocument:

    def test_create_txt_doc_returns_201(self, client, auth_headers, created_bot, sample_txt_file):
        files = {"file": ("test.txt", sample_txt_file, "text/plain")}
        data = {
            "doc_name": "test",
            "doc_type": ".txt",
            "doc_size": TEST_TXT_SIZE
        }

        response = client.post(
            f"{API_PREFIX}/bots/{created_bot["bot_id"]}/documents",
            files=files,
            data=data,
            headers=auth_headers
        )

        assert response.status_code == 201
        json_data = response.json()
        assert json_data["doc_name"] == "test"
        assert json_data["doc_type"] == ".txt"
        assert "doc_id" in json_data

        client.delete(
            f"{API_PREFIX}/bots/{created_bot["bot_id"]}/documents/{json_data['doc_id']}",
            headers=auth_headers
        )

    # add test for pdf and docx

    def test_create_doc_type_not_allowed_returns_400(self, client, auth_headers, created_bot, invalid_file_exe):
        files = {"file": ("malware.exe", invalid_file_exe, "application/x-msdownload")}
        data = {
            "doc_name": "malware",
            "doc_type": ".exe",
            "doc_size": 5
        }

        response = client.post(
            f"{API_PREFIX}/bots/{created_bot["bot_id"]}/documents",
            files=files,
            data=data,
            headers=auth_headers
        )

        assert response.status_code == 400
        assert "File type not allowed" in response.json()["detail"]

    def test_create_doc_size_exceeds_returns_400(self, client, auth_headers, created_bot, large_file):
        file_size = 11 * 1024 * 1024  # 11MB
        files = {"file": ("huge.txt", large_file, "text/plain")}
        data = {
            "doc_name": "huge",
            "doc_type": ".txt",
            "doc_size": file_size
        }

        response = client.post(
            f"{API_PREFIX}/bots/{created_bot["bot_id"]}/documents",
            files=files,
            data=data,
            headers=auth_headers
        )

        assert response.status_code == 400
        assert "File too large" in response.json()["detail"]

    def test_create_doc_duplicate_returns_409(self, client, auth_headers, created_bot, sample_txt_file):
        files = {"file": ("duplicate.txt", sample_txt_file, "text/plain")}
        data = {
            "doc_name": "duplicate",
            "doc_type": ".txt",
            "doc_size": TEST_TXT_SIZE
        }

        first_response = client.post(
            f"{API_PREFIX}/bots/{created_bot["bot_id"]}/documents",
            files=files,
            data=data,
            headers=auth_headers
        )
        assert first_response.status_code == 201
        doc_id = first_response.json()["doc_id"]

        sample_txt_file.seek(0)  # Reset file pointer
        second_response = client.post(
            f"{API_PREFIX}/bots/{created_bot["bot_id"]}/documents",
            files=files,
            data=data,
            headers=auth_headers
        )

        assert second_response.status_code == 409
        assert "Document already exists" in second_response.json()["detail"]

        client.delete(f"{API_PREFIX}/bots/{created_bot["bot_id"]}/documents/{doc_id}", headers=auth_headers)

    def test_create_doc_without_auth_returns_401(self, client, invalid_auth_headers, created_bot, sample_txt_file):
        files = {"file": ("test.txt", sample_txt_file, "text/plain")}
        data = {
            "doc_name": "test",
            "doc_type": ".txt",
            "doc_size": TEST_TXT_SIZE
        }

        response = client.post(
            f"{API_PREFIX}/bots/{created_bot["bot_id"]}/documents",
            files=files,
            data=data,
            headers=invalid_auth_headers
        )

        assert response.status_code == 401

    def test_create_doc_for_nonexistent_bot_returns_404(self, client, auth_headers, sample_txt_file):
        files = {"file": ("test.txt", sample_txt_file, "text/plain")}
        data = {
            "doc_name": "test",
            "doc_type": ".txt",
            "doc_size": TEST_TXT_SIZE
        }

        response = client.post(
            f"{API_PREFIX}/bots/{NONEXISTENT_BOT_ID}/documents",
            files=files,
            data=data,
            headers=auth_headers
        )

        assert response.status_code == 404
        assert "Bot not found" in response.json()["detail"]


class TestGetAllDocuments:

    def test_get_documents_returns_200_and_document_list(self, client, auth_headers, created_bot):
        response = client.get(
            f"{API_PREFIX}/bots/{created_bot["bot_id"]}/documents",
            headers=auth_headers
        )

        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_get_documents_without_auth_returns_401(self, client, invalid_auth_headers, created_bot):
        response = client.get(
            f"{API_PREFIX}/bots/{created_bot["bot_id"]}/documents",
            headers=invalid_auth_headers
        )

        assert response.status_code == 401

    def test_get_documents_for_nonexistent_bot_returns_404(self, client, auth_headers):
        response = client.get(
            f"{API_PREFIX}/bots/{NONEXISTENT_BOT_ID}/documents",
            headers=auth_headers
        )

        assert response.status_code == 404
        assert "Bot not found" in response.json()["detail"]


class TestGetDocumentById:

    def test_get_document_by_id_returns_200_and_document(self, client, auth_headers, created_document):
        bot_id = created_document["bot_id"]
        doc_id = created_document["doc_id"]

        response = client.get(
            f"{API_PREFIX}/bots/{bot_id}/documents/{doc_id}",
            headers=auth_headers
        )

        # Assert
        assert response.status_code == 200
        json_data = response.json()
        assert json_data["doc_id"] == doc_id
        assert json_data["bot_id"] == bot_id
        assert "doc_name" in json_data
        assert "doc_type" in json_data
        assert "doc_size" in json_data

    def test_get_document_by_id_without_auth_returns_401(self, client, invalid_auth_headers, created_document):
        bot_id = created_document["bot_id"]
        doc_id = created_document["doc_id"]

        response = client.get(
            f"{API_PREFIX}/bots/{bot_id}/documents/{doc_id}",
            headers=invalid_auth_headers
        )

        assert response.status_code == 401

    def test_get_document_by_id_for_nonexistent_bot_returns_404(self, client, auth_headers):
        doc_id = 1

        response = client.get(
            f"{API_PREFIX}/bots/{NONEXISTENT_BOT_ID}/documents/{doc_id}",
            headers=auth_headers
        )

        assert response.status_code == 404
        assert "Bot not found" in response.json()["detail"]

    def test_get_document_by_id_for_nonexistent_doc_returns_404(self, client, auth_headers, created_bot):
        response = client.get(
            f"{API_PREFIX}/bots/{created_bot["bot_id"]}/documents/{NONEXISTENT_DOC_ID}",
            headers=auth_headers
        )

        assert response.status_code == 404
        assert "Document not found" in response.json()["detail"]


class TestDownloadDocumentById:
    def test_download_document_by_id_returns_200_and_document(self, client, auth_headers, created_document):
        bot_id = created_document["bot_id"]
        doc_id = created_document["doc_id"]

        response = client.get(
            f"{API_PREFIX}/bots/{bot_id}/documents/{doc_id}/download",
            headers=auth_headers
        )

        assert response.status_code == 200
        assert response.content
        assert len(response.content) > 0
        assert "content-type" in response.headers

    def test_download_document_by_id_without_auth_returns_401(self, client, invalid_auth_headers, created_document):
        bot_id = created_document["bot_id"]
        doc_id = created_document["doc_id"]

        response = client.get(
            f"{API_PREFIX}/bots/{bot_id}/documents/{doc_id}/download",
            headers=invalid_auth_headers
        )

        assert response.status_code == 401

    def test_download_documents_by_id_for_nonexistent_bot_returns_404(self, client, auth_headers):
        doc_id = 1

        response = client.get(
            f"{API_PREFIX}/bots/{NONEXISTENT_BOT_ID}/documents/{doc_id}/download",
            headers=auth_headers
        )

        assert response.status_code == 404
        assert "Bot not found" in response.json()["detail"]

    def test_download_documents_by_id_for_nonexistent_doc_returns_404(self, client, auth_headers, created_bot):
        response = client.get(
            f"{API_PREFIX}/bots/{created_bot["bot_id"]}/documents/{NONEXISTENT_DOC_ID}/download",
            headers=auth_headers
        )

        assert response.status_code == 404
        assert "Document not found" in response.json()["detail"]


class TestDeleteDocumentById:
    def test_delete_document_by_id_returns_204(self, client, auth_headers, created_bot, sample_txt_file):
        files = {"file": ("delete_me.txt", sample_txt_file, "text/plain")}
        data = {
            "doc_name": "delete_me",
            "doc_type": ".txt",
            "doc_size": TEST_TXT_SIZE
        }
        create_response = client.post(
            f"{API_PREFIX}/bots/{created_bot["bot_id"]}/documents",
            files=files,
            data=data,
            headers=auth_headers
        )
        doc_id = create_response.json()["doc_id"]

        response = client.delete(
            f"{API_PREFIX}/bots/{created_bot["bot_id"]}/documents/{doc_id}",
            headers=auth_headers
        )

        assert response.status_code == 204
        assert response.content == b""  # No content

    def test_delete_document_by_id_for_nonexistent_bot_returns_404(self, client, auth_headers):
        doc_id = 1

        response = client.delete(
            f"{API_PREFIX}/bots/{NONEXISTENT_BOT_ID}/documents/{doc_id}",
            headers=auth_headers
        )

        assert response.status_code == 404
        assert "Bot not found" in response.json()["detail"]

    def test_delete_document_by_id_for_nonexistent_doc_returns_404(self, client, auth_headers, created_bot):
        response = client.delete(
            f"{API_PREFIX}/bots/{created_bot["bot_id"]}/documents/{NONEXISTENT_DOC_ID}",
            headers=auth_headers
        )

        assert response.status_code == 404
        assert "Document not found" in response.json()["detail"]

    def test_delete_document_by_id_without_auth_returns_401(self, client, invalid_auth_headers, created_document):
        bot_id = created_document["bot_id"]
        doc_id = created_document["doc_id"]

        response = client.delete(
            f"{API_PREFIX}/bots/{bot_id}/documents/{doc_id}",
            headers=invalid_auth_headers
        )

        assert response.status_code == 401

