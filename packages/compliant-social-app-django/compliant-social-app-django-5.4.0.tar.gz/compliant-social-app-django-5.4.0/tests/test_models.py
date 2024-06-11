from datetime import timedelta
from unittest import mock

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.db import IntegrityError
from django.test import TestCase

from compliant_social_django.models import (
    AbstractUserSocialAuth,
    Association,
    Code,
    DjangoStorage,
    Nonce,
    Partial,
    UserSocialAuth,
)


class TestSocialAuthUser(TestCase):
    def test_user_relationship_none(self):
        """Accessing User.social_user outside of the pipeline doesn't work"""
        User = get_user_model()
        user = User._default_manager.create_user(username="randomtester")
        with self.assertRaises(AttributeError):
            user.social_user

    def test_user_existing_relationship(self):
        """Accessing User.social_user outside of the pipeline doesn't work"""
        User = get_user_model()
        user = User._default_manager.create_user(username="randomtester")
        UserSocialAuth.objects.create(user=user, provider="my-provider", uid="1234")
        with self.assertRaises(AttributeError):
            user.social_user

    def test_get_social_auth(self):
        User = get_user_model()
        user = User._default_manager.create_user(username="randomtester")
        user_social = UserSocialAuth.objects.create(
            user=user, provider="my-provider", uid="1234"
        )
        other = UserSocialAuth.get_social_auth("my-provider", "1234")
        self.assertEqual(other, user_social)

    def test_get_social_auth_none(self):
        other = UserSocialAuth.get_social_auth("my-provider", "1234")
        self.assertIsNone(other)

    def test_cleanup(self):
        Code.objects.create(email="first@example.com")
        Code.objects.create(email="second@example.com")
        code = Code.objects.create(email="expire@example.com")
        code.timestamp -= timedelta(days=30)
        code.save()

        Partial.objects.create()
        partial = Partial.objects.create()
        partial.timestamp -= timedelta(days=30)
        partial.save()

        call_command("clearsocial")

        self.assertEqual(2, Code.objects.count())
        self.assertEqual(1, Partial.objects.count())


class TestUserSocialAuth(TestCase):
    def setUp(self):
        self.test_token = (
            "eyJzdWIiOjEwMDAsImlzcyI6Imh0dHBzOi8vYXV0aG9yaXphd"
            "Glvbi1zZXJ2ZXIuY29tIiwiY2lkIjoiaHR0cHM6Ly9leGF"
            "tcGxlLWFwcC5jb20iLCJpYXQiOjE0NzAwMDI3MDMsImV4c"
            "CI6MTUyOTE3NDg1MSwic2NvcGUiOiJyZWFkIHdyaXRlIn0"
        )
        self.encrypted_test_token = (
            b"vE4bSBeUzlOPG8MjK0QuITejoHEtAlJj5YCyzy+5SThQvjIX"
            b"jY8K4b5xdTc8sYAespdqfbHYWi4UiwMVlpOm1vJcVNAw+QpRSyQ6zp"
            b"PaiPz6wAWco7HmkG1TEJ2eHzQ3XiC5H0UBByhhgY4vzh824Djxn9u+"
            b"MOIZBcirRzWctYq3HQshGyzfe5BHqm51TrtC/En6tVwUpF5vCNQ2ez"
            b"mkGLBNDBKESnhY5QHapUwum1nb3RWlEMRBnR9wTZD8zufq"
        )

        self.user_model = get_user_model()
        self.user = self.user_model._default_manager.create_user(
            username="randomtester", email="user@example.com"
        )
        self.usa = UserSocialAuth.objects.create(
            user=self.user, provider="my-provider", uid="1234"
        )

    def _configure_mock_kms_client(self, field):
        field_object = self.usa._meta.get_field(field)
        mock_kms_client = mock.MagicMock()
        mock_kms_client.encrypt = mock.MagicMock(
            return_value={"CiphertextBlob": self.encrypted_test_token}
        )
        mock_kms_client.decrypt = mock.MagicMock(return_value=self.test_token)
        field_object._kms_client = mock_kms_client

    def test_changed(self):
        self.user.email = eml = "test@example.com"
        UserSocialAuth.changed(user=self.user)
        db_eml = self.user_model._default_manager.get(username=self.user.username).email
        self.assertEqual(db_eml, eml)

    def test_set_extra_data(self):
        self.usa.set_extra_data({"a": "b"})
        self.usa.refresh_from_db()
        db_data = UserSocialAuth.objects.get(id=self.usa.id).extra_data
        self.assertEqual(db_data, {"a": "b"})

    def test_mark_revoked(self):
        self.assertEqual(self.usa.revoked, False)
        self.usa.mark_revoked()
        self.assertEqual(self.usa.revoked, True)

    def test_clear_revoked(self):
        self._configure_mock_kms_client("actual_refresh_token")
        self.usa.mark_revoked()
        self.assertEqual(self.usa.revoked, True)

        new_access_token = "123"
        refresh_token = "abc"

        self.usa.actual_refresh_token = refresh_token
        self.usa.actual_access_token = "321"

        mock_backend = mock.MagicMock()
        self.usa.get_backend_instance = mock.MagicMock()
        self.usa.get_backend_instance.return_value = mock_backend
        mock_backend.extra_data.return_value = {"access_token": new_access_token}

        self.usa.refresh_token(mock.MagicMock())

        self.assertEqual(refresh_token, self.usa.actual_refresh_token)
        self.assertEqual(new_access_token, self.usa.actual_access_token)

        self.assertEqual(self.usa.revoked, False)

    def test_disconnect(self):
        m = mock.Mock()
        UserSocialAuth.disconnect(m)
        self.assertListEqual(m.method_calls, [mock.call.delete()])

    def test_username_field(self):
        self.assertEqual(UserSocialAuth.username_field(), "username")
        with mock.patch(
            "compliant_social_django.models.UserSocialAuth.user_model",
            return_value=mock.Mock(USERNAME_FIELD="test"),
        ):
            self.assertEqual(UserSocialAuth.username_field(), "test")

    def test_user_exists(self):
        self.assertTrue(UserSocialAuth.user_exists(username=self.user.username))
        self.assertFalse(UserSocialAuth.user_exists(username="test"))

    def test_get_username(self):
        self.assertEqual(UserSocialAuth.get_username(self.user), self.user.username)

    def test_create_user(self):
        # Catch integrity error and find existing user
        UserSocialAuth.create_user(username=self.user.username)

    def test_create_user_reraise(self):
        with self.assertRaises(IntegrityError):
            UserSocialAuth.create_user(username=self.user.username, email=None)

    @mock.patch(
        "compliant_social_django.models.UserSocialAuth.username_field",
        return_value="email",
    )
    @mock.patch(
        "django.contrib.auth.models.UserManager.create_user", side_effect=IntegrityError
    )
    def test_create_user_custom_username(self, *args):
        UserSocialAuth.create_user(username=self.user.email)

    @mock.patch("compliant_social_django.storage.transaction", spec=[])
    def test_create_user_without_transaction_atomic(self, *args):
        UserSocialAuth.create_user(username="test")
        self.assertTrue(
            self.user_model._default_manager.filter(username="test").exists()
        )

    def test_get_user(self):
        self.assertEqual(UserSocialAuth.get_user(pk=self.user.pk), self.user)
        self.assertIsNone(UserSocialAuth.get_user(pk=123))

    def test_get_users_by_email(self):
        qs = UserSocialAuth.get_users_by_email(email=self.user.email)
        self.assertEqual(qs.count(), 1)

    def test_get_social_auth(self):
        usa = self.usa
        # Model
        self.assertEqual(
            UserSocialAuth.get_social_auth(provider=usa.provider, uid=usa.uid), usa
        )
        self.assertIsNone(UserSocialAuth.get_social_auth(provider="a", uid=1))

        # Mixin
        self.assertEqual(
            super(AbstractUserSocialAuth, usa).get_social_auth(
                provider=usa.provider, uid=usa.uid
            ),
            usa,
        )
        self.assertIsNone(
            super(AbstractUserSocialAuth, usa).get_social_auth(provider="a", uid=1)
        )

        # Manager
        self.assertEqual(
            UserSocialAuth.objects.get_social_auth(provider=usa.provider, uid=usa.uid),
            usa,
        )
        self.assertIsNone(UserSocialAuth.objects.get_social_auth(provider="a", uid=1))

    def test_get_social_auth_for_user(self):
        qs = UserSocialAuth.get_social_auth_for_user(
            user=self.user, provider=self.usa.provider, id=self.usa.id
        )
        self.assertEqual(qs.count(), 1)

    def test_create_social_auth(self):
        usa = UserSocialAuth.create_social_auth(user=self.user, provider="test", uid=1)
        self.assertEqual(usa.uid, "1")
        self.assertEqual(str(usa), str(self.user))

    @mock.patch("compliant_social_django.storage.transaction", spec=[])
    def test_create_social_auth_without_transaction_atomic(self, *args):
        with self.assertRaises(IntegrityError):
            UserSocialAuth.create_social_auth(
                user=self.user, provider=self.usa.provider, uid=self.usa.uid
            )

    def test_username_max_length(self):
        self.assertEqual(UserSocialAuth.username_max_length(), 150)

    def test_access_token_field(self):
        self._configure_mock_kms_client("actual_access_token")

        self.assertIsNone(self.usa.actual_access_token)
        self.usa.actual_access_token = self.test_token
        self.assertEqual(self.usa.actual_access_token, self.test_token)
        self.usa.actual_access_token = None
        self.assertIsNone(self.usa.actual_access_token)

    def test_refresh_token_field(self):
        self._configure_mock_kms_client("actual_refresh_token")

        self.assertIsNone(self.usa.actual_refresh_token)
        self.usa.actual_refresh_token = self.test_token
        self.usa.save()
        self.assertEqual(self.usa.actual_refresh_token, self.test_token)
        self.usa.actual_refresh_token = None
        self.usa.save()
        self.assertIsNone(self.usa.actual_refresh_token)


class TestNonce(TestCase):
    def test_use(self):
        self.assertEqual(Nonce.objects.count(), 0)
        self.assertTrue(Nonce.use(server_url="/", timestamp=1, salt="1"))
        self.assertFalse(Nonce.use(server_url="/", timestamp=1, salt="1"))
        self.assertEqual(Nonce.objects.count(), 1)


class TestAssociation(TestCase):
    def test_store_get_remove(self):
        Association.store(
            server_url="/",
            association=mock.Mock(
                handle="a", secret=b"b", issued=1, lifetime=2, assoc_type="c"
            ),
        )

        qs = Association.get(handle="a")
        self.assertEqual(qs.count(), 1)
        self.assertEqual(qs[0].secret, "Yg==\n")

        Association.remove(ids_to_delete=[qs.first().id])
        self.assertEqual(Association.objects.count(), 0)


class TestCode(TestCase):
    def test_get_code(self):
        code1 = Code.objects.create(email="test@example.com", code="abc")
        code2 = Code.get_code(code="abc")
        self.assertEqual(code1, code2)
        self.assertIsNone(Code.get_code(code="xyz"))


class TestPartial(TestCase):
    def test_load_destroy(self):
        p = Partial.objects.create(token="x", backend="y", data={})
        self.assertEqual(Partial.load(token="x"), p)
        self.assertIsNone(Partial.load(token="y"))

        Partial.destroy(token="x")
        self.assertEqual(Partial.objects.count(), 0)


class TestDjangoStorage(TestCase):
    def test_is_integrity_error(self):
        self.assertTrue(DjangoStorage.is_integrity_error(IntegrityError()))
