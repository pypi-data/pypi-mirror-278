import os

URL = "https://skaff-analytics-backend-j6kutwcwdq-ew.a.run.app/post"
SCHEMA_VERSION = "0.1.0"
HAS_CONSENT_INFO = os.environ.get("SKAFF_INFO_TELEMETRY_CONSENT", True) != "False"
HAS_CONSENT_ERROR = os.environ.get("SKAFF_ERROR_TELEMETRY_CONSENT", True) != "False"
DEBUG = os.environ.get("SKAFF_PROBE_DEBUG")
