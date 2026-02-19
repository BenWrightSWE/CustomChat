from tests.conftest import API_PREFIX
from fastapi import status


class TestEmbedUserInput:
    def test_embed_user_input_returns_200(self, client, test_api_key, sample_user_input):
        response = client.post(
            f"{API_PREFIX}/embed/user_input",
            json={"user_input": sample_user_input},
            headers=test_api_key
        )

        assert response.status_code == status.HTTP_200_OK
        embedded_input = response.json()
        # print(embedded_input)
        assert isinstance(embedded_input["embedding"], list)
        assert len(embedded_input["embedding"]) > 0

    def test_embed_txt_doc_bad_api_key_returns_401(self, client, sample_user_input):
        response = client.post(
            f"{API_PREFIX}/embed/user_input",
            json={"user_input": sample_user_input},
            headers={"X-API-KEY": ""}
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestEmbedTxtDocument:

    def test_embed_txt_doc_returns_200_and_list(self, client, test_api_key, sample_txt_file):
        response = client.post(
            f"{API_PREFIX}/embed/txt",
            json={"document": sample_txt_file},
            headers=test_api_key
        )

        assert response.status_code == status.HTTP_200_OK
        embedded_vals = response.json()
        # print(embedded_vals)
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