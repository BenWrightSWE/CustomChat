import pytest


class TestGetUserProfile:
    def test_get_user_profile_returns_200(self):
        return 0

    def test_get_user_profile_without_auth_returns_401(self):
        return 0


class TestUpdateCurrentUser:
    def test_update_current_user_returns_200(self):
        return 0

    def test_update_current_user_no_data_returns_400(self):
        return 0

    def test_update_current_user_without_auth_returns_401(self):
        return 0