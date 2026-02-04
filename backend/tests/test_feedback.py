from tests.conftest import (
    NONEXISTENT_BOT_ID,
    NONEXISTENT_FB_ID,
    API_PREFIX
)
from app.core.supabase import supabase_admin
from fastapi import status


class TestCreateFeedback:
    def test_create_feedback_returns_201(self, client, auth_headers, created_bot, sample_feedback_data):
        response = client.post(
            f"{API_PREFIX}/bots/{created_bot["bot_id"]}/feedback",
            json=sample_feedback_data,
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_201_CREATED

    def test_create_feedback_for_nonexistent_bot_returns_404(self, client, auth_headers, sample_feedback_data):
        response = client.post(
            f"{API_PREFIX}/bots/{NONEXISTENT_BOT_ID}/feedback",
            json=sample_feedback_data,
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_create_feedback_without_auth_returns_401(
            self, client, invalid_auth_headers, created_bot, sample_feedback_data
    ):
        response = client.post(
            f"{API_PREFIX}/bots/{created_bot["bot_id"]}/feedback",
            json=sample_feedback_data,
            headers=invalid_auth_headers
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestGetAllFeedback:
    def test_get_all_feedback_returns_200_and_list(self, client, auth_headers, created_bot):
        response = client.get(
            f"{API_PREFIX}/bots/{created_bot["bot_id"]}/feedback",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.json(), list)

    def test_get_all_feedback_for_nonexistent_bot_returns_404(self, client, auth_headers):
        response = client.get(
            f"{API_PREFIX}/bots/{NONEXISTENT_BOT_ID}/feedback",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_all_feedback_without_auth_returns_401(self, client, invalid_auth_headers, created_bot):
        response = client.get(
            f"{API_PREFIX}/bots/{created_bot["bot_id"]}/feedback",
            headers=invalid_auth_headers
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestGetFeedbackById:
    def test_get_feedback_by_id_returns_200_and_object(self, client, auth_headers, created_bot, sample_feedback_data):
        set_up_response = client.post(
            f"{API_PREFIX}/bots/{created_bot["bot_id"]}/feedback",
            json=sample_feedback_data,
            headers=auth_headers
        )
        feedback = set_up_response.json()

        response = client.get(
            f"{API_PREFIX}/bots/{created_bot["bot_id"]}/feedback/{feedback["fb_id"]}",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        json_data = response.json()
        assert json_data["is_neg"] == True
        assert json_data["fb_desc"] == "Sample feedback data!"
        assert json_data["use_log"] == None

        supabase_admin.table("feedback").delete().eq("fb_id", json_data["fb_id"]).execute()

    def test_get_feedback_by_id_for_nonexistent_feedback_returns_404(self, client, auth_headers, created_bot):
        response = client.get(
            f"{API_PREFIX}/bots/{created_bot["bot_id"]}/feedback{NONEXISTENT_FB_ID}",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_feedback_by_id_for_nonexistent_bot_returns_404(self, client, auth_headers):
        response = client.get(
            f"{API_PREFIX}/bots/{NONEXISTENT_BOT_ID}/feedback{NONEXISTENT_FB_ID}",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_feedback_by_id_without_auth_returns_401(
            self, client, auth_headers, invalid_auth_headers, created_bot, sample_feedback_data
    ):
        set_up_response = client.post(
            f"{API_PREFIX}/bots/{created_bot["bot_id"]}/feedback",
            json=sample_feedback_data,
            headers=auth_headers
        )
        feedback = set_up_response.json()

        response = client.get(
            f"{API_PREFIX}/bots/{created_bot["bot_id"]}/feedback/{feedback["fb_id"]}",
            headers=invalid_auth_headers
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        supabase_admin.table("feedback").delete().eq("fb_id", feedback["fb_id"]).execute()