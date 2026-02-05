from tests.conftest import API_PREFIX
from fastapi import status


class TestEmbedTxtDocument:

    def test_embed_txt_doc_returns_200_and_list(self, client, test_api_key, sample_txt_file):
        response = client.post(
            f"{API_PREFIX}/embed/txt",
            json={"document": sample_txt_file},
            headers=test_api_key
        )

        print(response.json)
        assert response.status_code == status.HTTP_200_OK
        embedded_vals = response.json()
        assert isinstance(embedded_vals["embedding_objects"], list)
        assert len(embedded_vals["embedding_objects"]) > 0

    def test_embed_txt_doc_size_exceeds_returns_413(self, client, test_api_key, sample_large_txt_file):
        response = client.post(
            f"{API_PREFIX}/embed/txt",
            json={"document": sample_large_txt_file},
            headers=test_api_key
        )

        assert response.status_code == status.HTTP_413_CONTENT_TOO_LARGE

    def test_embed_txt_doc_bad_api_key_returns_401(self, client, sample_txt_file):
        response = client.post(
            f"{API_PREFIX}/embed/txt",
            json={"document": sample_txt_file},
            headers={"X-API-KEY": ""}
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED