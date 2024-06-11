from unittest.mock import MagicMock

from django.contrib.auth import get_user_model
from django.test import TestCase

from compliant_social_django.models import UserSocialAuth


class TestUsers(TestCase):
    def setUp(self):
        self.user_model = get_user_model()
        self.user = self.user_model.objects.create_user(
            username='randomtester', email='user@example.com')
        self.usa = UserSocialAuth.objects.create(
            user=self.user, provider='my-provider', uid='1234')

    def test_user_social_auth_actual_refresh_token_persists_after_calling_refresh_token(self):
        new_access_token = '123'
        refresh_token = 'abc'

        self.usa.actual_refresh_token = refresh_token
        self.usa.actual_access_token = '321'

        mock_backend = MagicMock()
        self.usa.get_backend_instance = MagicMock()
        self.usa.get_backend_instance.return_value = mock_backend
        mock_backend.extra_data.return_value = {'access_token': new_access_token}

        self.usa.refresh_token(MagicMock())

        self.assertEqual(refresh_token, self.usa.actual_refresh_token)
        self.assertEqual(new_access_token, self.usa.actual_access_token)

    def test_access_token_is_set_to_none_if_access_token_is_not_present_in_response(self):
        mock_backend = MagicMock()
        self.usa.get_backend_instance = MagicMock()
        self.usa.get_backend_instance.return_value = mock_backend
        mock_backend.extra_data.return_value = {}

        self.usa.refresh_token(MagicMock())

        self.assertIsNone(self.usa.actual_access_token)

    def test_user_social_auth_actual_refresh_token_gets_set(self):
        new_access_token = '123'
        new_refresh_token = 'abc'

        self.usa.actual_refresh_token = 'cba'
        self.usa.actual_access_token = '321'

        mock_backend = MagicMock()
        self.usa.get_backend_instance = MagicMock()
        self.usa.get_backend_instance.return_value = mock_backend
        mock_backend.extra_data.return_value = {
            'access_token': new_access_token,
            'refresh_token': new_refresh_token}

        self.usa.refresh_token(MagicMock())

        self.assertEqual(new_refresh_token, self.usa.actual_refresh_token)
        self.assertEqual(new_access_token, self.usa.actual_access_token)