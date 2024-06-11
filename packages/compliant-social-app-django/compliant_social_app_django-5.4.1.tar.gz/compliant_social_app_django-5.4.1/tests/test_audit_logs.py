from unittest.mock import patch

from django.test import TestCase
from social_core.backends.oauth import BaseOAuth2

from compliant_social_django.audit.clients import AbstractBaseAuditLogger
from compliant_social_django.decorators import create_audit_logs


class AuditLogsTestCase(TestCase):

    @patch.object(BaseOAuth2, "refresh_token")
    @patch.object(BaseOAuth2, "revoke_token")
    @patch.object(BaseOAuth2, "request_access_token")
    @patch.object(AbstractBaseAuditLogger, "log_request_token_event")
    @patch.object(AbstractBaseAuditLogger, "log_revoke_token_event")
    def test_audit_log_decorator(
        self,
        log_revoke_token_event,
        log_request_token_event,
        request_access_token,
        revoke_token,
        refresh_token,
    ):

        @create_audit_logs(AbstractBaseAuditLogger)
        class TestAuditLogBackend(BaseOAuth2):
            pass

        TestAuditLogBackend().request_access_token()
        TestAuditLogBackend().refresh_token("fake_token")
        TestAuditLogBackend().revoke_token("fake_token", "fake_uid")

        self.assertTrue(log_request_token_event.called)
        self.assertTrue(log_revoke_token_event.called)
