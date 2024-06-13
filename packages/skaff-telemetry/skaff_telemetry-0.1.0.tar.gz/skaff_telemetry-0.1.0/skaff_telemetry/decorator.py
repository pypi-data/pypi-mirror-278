import logging
import time
import traceback
import uuid
from functools import wraps
import json

import requests
from skaff_telemetry.config import DEBUG, HAS_CONSENT_ERROR, HAS_CONSENT_INFO, SCHEMA_VERSION, URL
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# Configure logging for the module
logging_level = logging.DEBUG if DEBUG else logging.INFO
logging.basicConfig(level=logging_level)
logger = logging.getLogger(__name__)

# Setup a retry strategy for HTTP requests that disables retries by setting all counts to 0.
retry_strategy = Retry(total=0, connect=0, read=0, redirect=0, status=0)

# Configure an HTTPAdapter with the no-retry strategy and mount it to a session.
adapter = HTTPAdapter(max_retries=retry_strategy)
session = requests.Session()
session.mount("http://", adapter)
session.mount("https://", adapter)


def skaff_telemetry(timeout=10, **dec_kwargs):
    """
    Decorator for adding telemetry sending capability to functions.

    Args:
        timeout (int): The timeout in seconds for the telemetry HTTP POST request.
        **dec_kwargs: Additional keyword arguments to be passed as telemetry data.

    Returns:
        A decorator function that wraps the original function, adding telemetry
        sending functionality before and after its execution, and on exception.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            """Wraps the decorated function, sending telemetry data on its invocation."""
            data = {**dec_kwargs, "function_name": func.__qualname__}
            try:
                result = func(*args, **kwargs)
                if HAS_CONSENT_INFO:
                    event_type = "INVOKE"
                    _send_telemetry(data=data, event_type=event_type, timeout=timeout)
            except Exception as e:
                if HAS_CONSENT_ERROR:
                    event_type = "ERROR"
                    content = {
                        "error": f"{e}",
                        "error_traceback": traceback.format_exc(),
                    }
                    _send_telemetry(
                        data=data,
                        content=json.dump(content),
                        event_type=event_type,
                        timeout=timeout,
                    )
                raise
            return result

        return wrapper

    return decorator


def _send_telemetry(data, event_type, content=None, timeout=10):
    """
    Sends telemetry data to a predefined URL using a POST request.

    Args:
        data (dict): The JSON data to send as part of the telemetry.
        event_type (str): The type of event to report in the telemetry (e.g., "INVOKE", "ERROR").
        content (dict, optional): Additional content to include in the telemetry report.
        timeout (int): The timeout in seconds for the HTTP POST request.
    """
    start_time = time.perf_counter()

    payload = construct_payload(data, event_type, content)

    try:
        response = session.post(URL, json=payload, timeout=timeout)
        logger.info(
            f"HTTP POST Request to {URL} performed. Status Code: {response.status_code}, Response: {response.text}"
        )
    except Exception as e:
        logger.info(f"A problem occurred when trying to send telemetry: {e}")

    end_time = time.perf_counter()
    logger.debug(f"Telemetry send execution time: {end_time - start_time} seconds")


def construct_payload(data, event_type, content):
    """Helper function to construct the telemetry payload."""
    return {
        **data,
        "invocation_id": str(uuid.uuid4())[:8],
        "schema_version": SCHEMA_VERSION,
        "event_type": event_type,
        "content": content,
    }
