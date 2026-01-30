from backend.tests.conftest import API_PREFIX

class TestGetUserProfile:

    def test_get_user_profile_returns_200(self, client, auth_headers):
        response = client.get(
            f"{API_PREFIX}/me",
            headers=auth_headers
        )

        assert response.status_code == 200

    def test_get_user_profile_without_auth_returns_401(self, client, invalid_auth_headers):
        response = client.get(
            f"{API_PREFIX}/me",
            headers=invalid_auth_headers
        )

        assert response.status_code == 401


class TestUpdateCurrentUser:

    def test_update_current_user_returns_200_and_user(self, client, auth_headers):
        update_info = {"first_name": "Jane"}

        response = client.patch(
            f"{API_PREFIX}/me",
            json=update_info,
            headers=auth_headers
        )

        assert response.status_code == 200
        json_data = response.json()
        assert json_data["first_name"] == "Jane"
        assert json_data["last_name"] == "Doe"
        assert json_data["company"] == "DoubleOSeven"
        assert json_data["email"] == "test@example.com"
        assert json_data["phone"] == "1234567890"

    def test_update_current_user_no_data_returns_400(self, client, auth_headers):
        update_info = {}

        response = client.patch(
            f"{API_PREFIX}/me",
            json=update_info,
            headers=auth_headers
        )

        assert response.status_code == 400

    def test_update_current_user_without_auth_returns_401(self, client, invalid_auth_headers):
        update_info = {"first_name": "Jane"}

        response = client.patch(
            f"{API_PREFIX}/me",
            json=update_info,
            headers=invalid_auth_headers
        )

        assert response.status_code == 401


class TestUpdateUserEmail:
    def test_update_user_email_returns_200(self, client, auth_headers):
        response = client.patch(
            f"{API_PREFIX}/me/email",
            json={"email": "updatetest@example.com"},
            headers=auth_headers
        )

        assert response.status_code == 200
        assert response.json()["message"] == "Email updated successfully"

        response = client.patch(
            f"{API_PREFIX}/me/email",
            json={"email": "test@example.com"},
            headers=auth_headers
        )

    def test_update_current_user_without_auth_returns_401(self, client, invalid_auth_headers):
        update_info = {"first_name": "Jane"}

        response = client.patch(
            f"{API_PREFIX}/me/email",
            json=update_info,
            headers=invalid_auth_headers
        )

        assert response.status_code == 401
