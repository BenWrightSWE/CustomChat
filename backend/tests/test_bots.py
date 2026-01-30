from backend.tests.conftest import NONEXISTENT_BOT_ID, API_PREFIX


class TestCreateBot:
    def test_create_bot_returns_201_and_bot(self, client, auth_headers, sample_bot_data):
        response = client.post(
            f"{API_PREFIX}/bots",
            json=sample_bot_data,
            headers=auth_headers
        )

        assert response.status_code == 201
        json_data = response.json()
        assert json_data["bot_name"] == "Test Bot"
        assert json_data["bot_desc"] == "A bot for testing"
        assert json_data["avatar"] == "base"
        assert json_data["color"] == "tan"
        assert json_data["storage"] == 0
        assert json_data["uses"] == 0
        assert "bot_id" in json_data

    def test_create_bot_without_auth_returns_401(self, client, invalid_auth_headers, sample_bot_data):
        response = client.post(
            f"{API_PREFIX}/bots",
            json=sample_bot_data,
            headers=invalid_auth_headers
        )

        assert response.status_code == 401

    # add test to validation part where it checks if bot data is complete.


class TestGetAllBots:
    def test_get_all_bots_returns_200_and_bot_list(self, client, auth_headers):
        # perhaps make bots to show up in the bot get, if you do make sure to clean it up as well.

        response = client.get(
            f"{API_PREFIX}/bots",
            headers=auth_headers
        )

        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_get_all_bots_without_auth_returns_401(self, client, invalid_auth_headers, sample_bot_data):
        response = client.get(
            f"{API_PREFIX}/bots",
            headers=invalid_auth_headers
        )

        assert response.status_code == 401


class TestGetBotById:
    def test_get_bot_by_id_returns_200_and_bot(self, client, auth_headers, created_bot):
        response = client.get(
            f"{API_PREFIX}/bots/{created_bot["bot_id"]}",
            headers=auth_headers
        )

        assert response.status_code == 200
        json_data = response.json()
        assert json_data["bot_name"] == "Test Bot"
        assert json_data["bot_desc"] == "A bot for testing"
        assert json_data["avatar"] == "base"
        assert json_data["color"] == "tan"
        assert json_data["storage"] == 0
        assert json_data["uses"] == 0
        assert "bot_id" in json_data

    def test_get_bot_by_id_for_nonexistent_bot_returns_404(self, client, auth_headers):
        response = client.get(
            f"{API_PREFIX}/bots/{NONEXISTENT_BOT_ID}",
            headers=auth_headers
        )

        assert response.status_code == 404

    def test_get_bot_by_id_without_auth_returns_401(self, client, invalid_auth_headers, created_bot):
        response = client.get(
            f"{API_PREFIX}/bots/{created_bot["bot_id"]}",
            headers=invalid_auth_headers
        )

        assert response.status_code == 401


class TestUpdateBotByID:
    def test_update_bot_by_id_single_val_returns_200_and_updated_val(self, client, auth_headers, created_bot):
        update_data = {"bot_name": "Updated Bot"}

        response = client.patch(
            f"{API_PREFIX}/bots/{created_bot["bot_id"]}",
            json=update_data,
            headers=auth_headers
        )

        json_data = response.json()
        print(json_data)

        assert response.status_code == 200
        assert json_data["bot_name"] == "Updated Bot"
        assert json_data["bot_desc"] == "A bot for testing"
        assert json_data["avatar"] == "base"
        assert json_data["color"] == "tan"
        assert json_data["storage"] == 0
        assert json_data["uses"] == 0

    def test_update_bot_by_id_all_vals_returns_200_and_updated_vals(self, client, auth_headers, created_bot):
        update_data = {
            "bot_name": "Updated Bot",
            "bot_desc": "An updated bot",
            "avatar": "default",
            "color": "charcoal",
            "storage": 1,
            "uses": 1,
        }

        response = client.patch(
            f"{API_PREFIX}/bots/{created_bot["bot_id"]}",
            json=update_data,
            headers=auth_headers
        )

        json_data = response.json()
        print(json_data)

        assert response.status_code == 200
        assert json_data["bot_name"] == "Updated Bot"
        assert json_data["bot_desc"] == "An updated bot"
        assert json_data["avatar"] == "default"
        assert json_data["color"] == "charcoal"
        assert json_data["storage"] == 1
        assert json_data["uses"] == 1

    def test_update_bot_by_id_no_data_returns_400(self, client, auth_headers, created_bot):
        update_data = {}

        response = client.patch(
            f"{API_PREFIX}/bots/{created_bot["bot_id"]}",
            json=update_data,
            headers=auth_headers
        )

        assert response.status_code == 400

    def test_update_bot_by_id_for_nonexistent_bot_returns_404(self, client, auth_headers):
        update_data = {"bot_name": "Updated Bot"}

        response = client.patch(
            f"{API_PREFIX}/bots/{NONEXISTENT_BOT_ID}",
            json=update_data,
            headers=auth_headers
        )

        assert response.status_code == 404

    def test_update_bot_by_id_without_auth_returns_401(self, client, invalid_auth_headers, created_bot):
        update_data = {"bot_name": "Updated Bot"}

        response = client.patch(
            f"{API_PREFIX}/bots/{created_bot["bot_id"]}",
            json=update_data,
            headers=invalid_auth_headers
        )

        assert response.status_code == 401


class TestDeleteBotByID:
    def test_delete_bot_by_id_returns_204(self, client, auth_headers, sample_bot_data):
        set_up_response = client.post(f"{API_PREFIX}/bots", json=sample_bot_data, headers=auth_headers)
        bot = set_up_response.json()

        response = client.delete(
            f"{API_PREFIX}/bots/{bot["bot_id"]}",
            headers=auth_headers
        )

        assert response.status_code == 204

    def test_delete_bot_by_id_for_nonexistent_bot_returns_404(self, client, auth_headers):
        response = client.delete(
            f"{API_PREFIX}/bots/{NONEXISTENT_BOT_ID}",
            headers=auth_headers
        )

        assert response.status_code == 404

    def test_delete_bot_by_id_without_auth_returns_401(
            self, client, auth_headers, invalid_auth_headers, sample_bot_data
    ):
        set_up_response = client.post(f"{API_PREFIX}/bots", json=sample_bot_data, headers=auth_headers)
        bot = set_up_response.json()

        response = client.delete(
            f"{API_PREFIX}/bots/{bot["bot_id"]}",
            headers=invalid_auth_headers
        )

        assert response.status_code == 401
