# coding: utf-8
""" 
  Copyright (c) 2024 Vipas.AI
 
  All rights reserved. This program and the accompanying materials
  are made available under the terms of a proprietary license which prohibits
  redistribution and use in any form, without the express prior written consent
  of Vipas.AI.
  
  This code is proprietary to Vipas.AI and is protected by copyright and
  other intellectual property laws. You may not modify, reproduce, perform,
  display, create derivative works from, repurpose, or distribute this code or any portion of it
  without the express prior written permission of Vipas.AI.
  
  For more information, contact Vipas.AI at legal@vipas.ai
"""  # noqa: E501
import os
from urllib.parse import unquote
from vipas.exceptions import ClientException

class Config:
    """This class contains various settings of the vipas API client.

    :param vps_auth_token: Variable to store the API key for a particular user.

    Example:
    config = Configuration(
       vps_auth_token = <your_api_key>
    )

    """

    def __init__(self, vps_auth_token=None) -> None:
        """
            Constructor for the configuration class
        """
        self.host = "https://proxy.vipas.dev" 
        """
            Default Host for the proxy service.
        """

        # Authentication Settings
        self.vps_auth_token = None
        if vps_auth_token:
            self.vps_auth_token = vps_auth_token
        """
            Variable to store API key for a particular user.
        """

        if not self.vps_auth_token:
            self.setup_api_key()

    def setup_api_key(self):
        """Set up API key based on environment."""
        env_type = os.getenv("VPS_ENV_TYPE")
        if env_type == "vipas-streamlit":
            self.host = "https://ix41nuuq3c-vpce-0c3dea8dfd371e6a1.execute-api.ap-south-1.amazonaws.com/v1" 
            self.vps_auth_token = self.extract_websocket_api_key()
        else:
            self.vps_auth_token = os.getenv("VPS_AUTH_TOKEN")
            if self.vps_auth_token is None or len(self.vps_auth_token) == 0:
                raise ClientException(400, "VPS_AUTH_TOKEN is not set in the environment variables or it is empty")

    def extract_websocket_api_key(self):
        """Extract API key from WebSocket headers in Streamlit."""
        try:
            from streamlit.web.server.websocket_headers import _get_websocket_headers
            headers = _get_websocket_headers()
            if headers and 'Cookie' in headers:
                cookie_string = headers['Cookie']
                cookies = {k.strip(): unquote(v.strip()) for k, v in 
                        (cookie.split('=') for cookie in cookie_string.split(';'))}
                
                if 'vps-auth-token' in cookies and len(cookies['vps-auth-token']) > 0:
                    return cookies['vps-auth-token']
                else:
                    raise ClientException(401, "vps-auth-token is not set in the WebSocket headers or it is empty")
            else:
                raise ClientException(400, "No cookies in WebSocket headers")
        except ImportError:
            raise ClientException(500, "Failed to import streamlit module")
        except Exception as e:
            raise ClientException(500, str(e))

    def get_vps_auth_token(self):
        """
            Gets API key for a particular user.
        """
        if self.vps_auth_token is not None:
            return self.vps_auth_token
        return None
