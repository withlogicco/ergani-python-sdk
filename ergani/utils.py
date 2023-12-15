import json

from requests.models import Response


def extract_error_message(response: Response) -> str:
    """
    Extracts the error message from a requests Response object.
    """
    content_type: str = response.headers.get("Content-Type", "")

    if "application/json" in content_type:
        try:
            response_data = response.json()
            if "message" in response_data:
                return response_data["message"]
            if "msg" in response_data:
                return response_data["msg"]
            if "detail" in response_data:
                return response_data["detail"]
            if not response_data:
                return ""
            return response_data
        except json.JSONDecodeError:
            pass

    if "text/plain" in content_type:
        return response.text.strip()

    return ""
