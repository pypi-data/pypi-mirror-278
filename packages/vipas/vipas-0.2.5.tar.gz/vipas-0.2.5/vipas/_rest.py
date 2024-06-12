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
import json
import httpx
import asyncio

from vipas.exceptions import ClientException

class RESTClientObject:
    def __init__(self, configuration) -> None:
        timeout = httpx.Timeout(300.0) # All requests will timeout after 300 seconds in all operations
        self.client = httpx.AsyncClient(timeout=timeout)

    async def request(self, method, url, headers=None, body=None):
        """Perform requests.

        :param method: http request method
        :param url: http request url
        :param headers: http request headers
        :param body: request json body, for `application/json`
        """
        method = method.upper()

        # Prepare headers and body for the request
        headers = headers or {}

        if body is not None:
            body = json.dumps(body)

        # Exponential backoff settings
        attempts = 4  # Exponential backoff retry attempts
        sleep_times = [0, 3, 6, 9]  # Exponential backoff retry sleep times in seconds
    
        for attempt in range(attempts):
            # Wait before the next attempt
            await asyncio.sleep(sleep_times[attempt])

            # Make the HTTP request using httpx
            try:
                predict_response = await self.client.request(method, url, headers=headers, content=body)
                predict_response.raise_for_status()
                predict_data = predict_response.json()

            except httpx.HTTPStatusError as e:
                if predict_response.status_code == 504:
                    if attempt < attempts - 1:
                        continue
                    else:
                        raise ClientException.from_response(http_resp=predict_response, body="Gateway Timeout occurred, please try again", data=None)
                
                error_detail = predict_response.json().get('detail', predict_response.text)
                raise ClientException.from_response(http_resp=predict_response, body=error_detail, data=None)
            
            except httpx.RequestError as e:
                # Handle any errors that occur while making the request
                raise ClientException(status=502, body="Request Error occurred, please try again", data=None)
            except Exception as e:
                # Handle any other exceptions that may occur
                raise ClientException(status=500, body="Unexpected error occurred, please try again", data=None)
            
            payload_type = predict_data.get("payload_type", None)
            if payload_type == "url":
                try:
                    output_data_response = await self.client.request("GET", predict_data.get("payload_url"))
                    output_data_response.raise_for_status()
                    output_data = output_data_response.json()

                    extractor = predict_data.get("extractor", None)
                    if extractor is not None:
                        # Define the function and execute the logic from the schema string
                        local_vars = {'output_data': output_data}
                        exec(extractor, globals(), local_vars)
                        output_data = local_vars['extracted_output_data']
                    
                    return output_data
                except httpx.HTTPStatusError as e:
                    error_detail = output_data_response.json().get('detail', output_data_response.text)
                    raise ClientException.from_response(http_resp=output_data_response, body=error_detail, data=None)
                
                except httpx.RequestError as e:
                    # Handle any errors that occur while making the request
                    raise ClientException(status=502, body="Request Error occurred, please try again", data=None)
                
                except Exception as e:
                    # Handle any other exceptions that may occur
                    raise ClientException(status=500, body="Unexpected error occurred, please try again", data=None)
            elif payload_type == "content":
                return predict_data.get("output_data", None)
            else:
                raise ClientException(status=500, body="Unexpected error occurred, please try again", data=None)
            

