from tests.unit.conftest import NONEXISTENT_BOT_ID, API_PREFIX
from fastapi import status


class TestBotContextualResponse:
    def test_bot_contextual_response_returns_200_and_response(
        self, client, created_bot, sample_assistant_request,
    ):
        response = client.post(
            f"{API_PREFIX}/bots/{created_bot["bot_id"]}/assistant",
            json=sample_assistant_request
        )

        assert response.status_code == status.HTTP_200_OK

    def test_bot_contextual_response_for_nonexistent_bot_returns_404(
        self, client, sample_assistant_request,
    ):
        response = client.post(
            f"{API_PREFIX}/bots/{NONEXISTENT_BOT_ID}/assistant",
            json=sample_assistant_request
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
