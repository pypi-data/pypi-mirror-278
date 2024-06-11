from typing import Type

from social_core.backends.oauth import BaseOAuth2

from .audit.clients import AbstractBaseAuditLogger


def create_audit_logs(audit_logger_class: Type[AbstractBaseAuditLogger]):
    """
    A decorator which injects audit logs into a social_core backend object.

    Attributes:
        audit_logger    An instantiated instance of an audit logger which inherits from
                        compliant_social_django.audit.clients.AbstractBaseAuditLogger
    """
    def decorator(backend: BaseOAuth2):
        original_request_access_token = backend.request_access_token
        original_refresh_token = backend.refresh_token
        original_revoke_token = backend.revoke_token

        audit_logger = audit_logger_class()

        def new_request_access_token(self, *args, **kwargs):
            json = original_request_access_token(self, *args, **kwargs)
            audit_logger.log_request_token_event(self.name, None, json['access_token'])
            return json

        def new_refresh_token(self, token, *args, **kwargs):
            audit_logger.log_request_token_event(self.name, kwargs.get('user_id', None), token)
            return original_refresh_token(self, token, *args, **kwargs)

        def new_revoke_token(self, token, uid, user_id=None):
            revoke_token_successful = original_revoke_token(self, token, uid)
            if revoke_token_successful:
                audit_logger.log_revoke_token_event(self.name, user_id, token)
            return revoke_token_successful

        backend.request_access_token = new_request_access_token
        backend.refresh_token = new_refresh_token
        backend.revoke_token = new_revoke_token
        return backend

    return decorator
