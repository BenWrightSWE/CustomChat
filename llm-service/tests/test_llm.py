from tests.conftest import API_PREFIX
from fastapi import status


class TestLLMResponseWithContext:

    def test_llm_response_with_context_returns_200(
            self, client, test_api_key, sample_user_input, sample_context, sample_history
    ):

        llm_request = {
            "chat_history": sample_history,
            "input_context": sample_context,
            "user_input": sample_user_input
        }

        response = client.post(
            f"{API_PREFIX}/llm/response",
            json=llm_request,
            headers=test_api_key
        )

        assert response.status_code == status.HTTP_200_OK
        llm_response = response.json()
        assert isinstance(llm_response["response"], str)
        print(llm_response["response"])

    def test_llm_response_with_no_user_input_returns_400(self, client, test_api_key, sample_context, sample_history):
        llm_request = {
            "chat_history": sample_history,
            "input_context": sample_context,
            "user_input": " "
        }

        response = client.post(
            f"{API_PREFIX}/llm/response",
            json=llm_request,
            headers=test_api_key
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_llm_response_with_more_than_max_context_returns_400(
            self, client, test_api_key, sample_user_input, sample_history
    ):

        llm_request = {
            "chat_history": sample_history,
            "input_context": ["1", "2", "3", "4", "5", "6"],
            "user_input": sample_user_input
        }

        response = client.post(
            f"{API_PREFIX}/llm/response",
            json=llm_request,
            headers=test_api_key
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_embed_txt_doc_bad_api_key_returns_401(
            self, client, sample_user_input, sample_context, sample_history
    ):
        llm_request = {
            "chat_history": sample_history,
            "input_context": sample_context,
            "user_input": sample_user_input
        }

        response = client.post(
            f"{API_PREFIX}/llm/response",
            json=llm_request,
            headers={"X-API-KEY": ""}
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
