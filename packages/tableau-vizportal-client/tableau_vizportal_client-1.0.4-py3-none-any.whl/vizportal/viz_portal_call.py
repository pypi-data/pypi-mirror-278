import requests
import json
import logging
from typing import Dict, Union, Any
from tableauserverclient import Server
from vizportal.payload import PayloadBuilder

CACHE_CONTROL: str = "no-cache"
ACCEPT: str = "application/json, text/plain, */*"
X_XSRF_TOKEN: str = ""
CONTENT_TYPE: str = "application/json;charset=UTF-8"
REQUEST_METHOD: str = "POST"


class VizPortalCall:
    """This class implements the call to the vizportal API.

    ...

    Attributes
    ----------
    server : Server
        The Tableau Server object.

    Methods
    -------
    call(payload: Dict[str, Union[str, Dict[str, Any]]]) -> Dict[str, Union[str, int]]
        Makes a call to the vizportal API.
    """

    def __init__(self, server: Server):
        # Assign the server object to the object's server attribute
        self.server: Server = server

    def _make_common_headers(self) -> Dict[str, Any]:
        """Makes the common headers for the request"""
        headers: Dict[str, str] = {}
        headers["cache-control"] = CACHE_CONTROL
        headers["accept"] = ACCEPT
        headers["x-xsrf-token"] = X_XSRF_TOKEN
        headers["content-type"] = CONTENT_TYPE
        headers["cookie"] = f"workgroup_session_id={self.server.auth_token}; XSRF-TOKEN="
        return headers
    
    def _payload_builder(self, payload: Union[PayloadBuilder, Dict[str, Any]]) -> Dict[str, Any]:
        """Checks if the payload is a PayloadBuilder object and builds it if it is.
        else creates a PayloadBuilder object from the dict and returns the payload."""
        if isinstance(payload, PayloadBuilder):
            return payload.payload
        elif isinstance(payload, dict):
            _payload = PayloadBuilder(payload)
            return _payload.payload
        else:
            raise Exception("Payload must be a PayloadBuilder or a Dict.")
    
    def make_request(self, payload: Union[PayloadBuilder, Dict[str, Any]]) -> Dict[str, Any]:
        """Makes a call to the vizportal API"""
        logging.debug(f"Sending request to {self.server.server_address}")
        payload = self._payload_builder(payload)
        endpoint = payload.get("method")
        url = f"{self.server.server_address}/vizportal/api/web/v1/{endpoint}"
        json_payload = json.dumps(payload)
        headers = self._make_common_headers()

        response = requests.request(
            REQUEST_METHOD, url, headers=headers, data=json_payload, verify=False
        )
        logging.debug(f"Response status code: {response.status_code}")
        if response.status_code != 200:
            logging.error(f"Response: {response.text}")
            raise Exception(f"Response: {response.text}")

        return response.json()
