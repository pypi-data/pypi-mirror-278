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
import pybreaker
import json
import asyncio
from typing import Tuple, Optional, List, Dict, Any
from pydantic import Field, StrictStr
from typing_extensions import Annotated
from ratelimit import limits, sleep_and_retry

from vipas.config import Config
from vipas import _rest
from vipas.exceptions import (
    ClientException
)

RequestSerialized = Tuple[str, str, Dict[str, str], Optional[any]]

class ModelClient:
    """
        Model client for Vipas API proxy service.
        :param config: .Configuration object for this client
    """
    def __init__(
        self,
        configuration=None
    ) -> None:
        # use default configuration if none is provided
        if configuration is None:
            configuration = Config()
        self.configuration = configuration

        self.rest_client = _rest.RESTClientObject(configuration)
        self._configure_decorators()

    def _configure_decorators(self):
        vps_env_type = os.getenv('VPS_ENV_TYPE')
        if vps_env_type == 'vipas-streamlit':
            self.rate_limit = lambda func: func  # No-op decorator
            self.breaker = pybreaker.CircuitBreaker(fail_max=20, reset_timeout=60)  # 20 failures per minute
        else:
            self.breaker = pybreaker.CircuitBreaker(fail_max=10, reset_timeout=60)  # 10 failures per minute
            self.rate_limit = limits(calls=20, period=60)  # 20 calls per minute
        
        # Apply decorators dynamically
        self.predict = self.breaker(self.predict)
        self.predict = self.rate_limit(self.predict)
        self.predict = sleep_and_retry(self.predict)

    def predict(
        self,
        model_id: Annotated[StrictStr, Field(description="Unique identifier for the model from which the prediction is requested")],
        input_data: Annotated[Any, Field(description="Input for the prediction")],
    ) -> dict:
        """
            Get Model Prediction

            Retrieves predictions from a specified model based on the provided input data. This endpoint is useful for generating real-time predictions from machine learning models.

            :param model_id: Unique identifier for the model from which the prediction is requested (required)
            :type model_id: str
            :return: Returns the result object.
        """
        # Validate input data size
        self._validate_input_data_size(input_data)

        _param = self._predict_serialize(
            model_id=model_id,
            input_data=input_data
        )

        response_data = asyncio.run(self._call_api(
            *_param,
        ))

        return response_data


    def _predict_serialize(
        self,
        model_id,
        input_data
    ) -> RequestSerialized:

        _query_params: List[Tuple[str, str]] = []
        _header_params: Dict[str, Optional[str]] =  {}
        _body: Any = None

        if model_id is not None:
            _query_params.append(('model_id', model_id))
        
        if input_data is not None:
            _body = input_data

        # set the HTTP header `Accept`
        _header_params['Accept'] = '*/*'
        _header_params['vps-auth-token'] = self.configuration.get_vps_auth_token()
        print("VPS_AUTH_TOKEN: ", self.configuration.get_vps_auth_token())

        return self._param_serialize(
            method='POST',
            resource_path='/predict',
            query_params=_query_params,
            header_params=_header_params,
            body=_body
        )

    def _param_serialize(
        self,
        method,
        resource_path,
        query_params=None,
        header_params=None,
        body=None
    ) -> RequestSerialized:

        """Builds the HTTP request params needed by the request.
        :param method: Method to call.
        :param resource_path: Path to method endpoint.
        :param query_params: Query parameters in the url.
        :param header_params: Header parameters to be
            placed in the request header.
        :param body: Request body.
        """
        # request url
        url = self.configuration.host + resource_path

        # query parameters
        if query_params:
            url_query = self._parameters_to_url_query(query_params)
            url += "?" + url_query

        return method, url, header_params, body
    
    def _parameters_to_url_query(self, params):
        """Get parameters as list of tuples, formatting collections.

        :param params: Parameters as dict or list of two-tuples
        :return: URL query string (e.g. a=Hello%20World&b=123)
        """

        return "&".join(["=".join(map(str, item)) for item in params])

    async def _call_api(
        self,
        method,
        url,
        header_params=None,
        body=None
    ) -> dict:
        """Makes the HTTP request (synchronous)
        :param method: Method to call.
        :param url: Path to method endpoint.
        :param header_params: Header parameters to be
            placed in the request header.
        :param body: Request body.
        :return: dict of response data.
        """

        try:
            # perform request and return response
            response_data = await self.rest_client.request(
                method, url,
                headers=header_params,
                body=body
            )

        except ClientException as e:
            raise e

        return response_data
    
    def _validate_input_data_size(self, input_data):
        """
        Validates that the size of input_data is less than 10 MB.

        :param input_data: The data to validate.
        :raises ClientException: If the input_data size is greater than 10 MB.
        """
        max_size_mb = 10
        max_size_bytes = max_size_mb * 1024 * 1024  # Convert MB to bytes

        if isinstance(input_data, str):
            input_size = len(input_data)
        elif isinstance(input_data, bytes):
            input_size = len(input_data)
        elif isinstance(input_data, (list, dict)):
            input_size = len(json.dumps(input_data))
        else:
            # Convert other types to string and check their length
            input_size = len(str(input_data))


        if input_size > max_size_bytes:
            raise ClientException(400, f"Payload size more than {max_size_mb} MB is not allowed.")

    

    