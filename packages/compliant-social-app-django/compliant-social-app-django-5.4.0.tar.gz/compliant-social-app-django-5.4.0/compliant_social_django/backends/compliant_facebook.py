from social_core.backends.facebook import FacebookOAuth2

from ..decorators import create_audit_logs
from ..storage import AuditLogger


@create_audit_logs(AuditLogger)
class CompliantFacebookOAuth2(FacebookOAuth2):
    pass
