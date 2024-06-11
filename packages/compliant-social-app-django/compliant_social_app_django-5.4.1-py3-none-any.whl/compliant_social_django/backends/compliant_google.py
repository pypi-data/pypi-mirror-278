from social_core.backends.google import GoogleOAuth2

from ..decorators import create_audit_logs
from ..storage import AuditLogger


@create_audit_logs(AuditLogger)
class CompliantGoogleOAuth2(GoogleOAuth2):
    pass
