import os
from typing import Iterator, Dict, Optional, Any, List
import requests
import time
import httpx
from httpx_sse import connect_sse
import logging
import asyncio
from aiohttp_sse_client import client as sse_client
import aiohttp
from rockai_cli_app.server.types import File,Path,Input,ConcatenateIterator
from pydantic import BaseModel
from rockai_cli_app.predictor import BasePredictor

logging.basicConfig(level=logging.DEBUG)

__all__ = [
    "BaseModel",
    "BasePredictor",
    "ConcatenateIterator",
    "File",
    "Input",
    "Path"
]

# client for rock AI
class Client:

    def __init__(self, api_token: str = None):
        self.api_token = (
            api_token if api_token is not None else os.environ.get("ROCK_API_TOKEN")
        )
        # Local testing
        # self.predict_url = "http://localhost:8000/v1/predictions"
        # self.get_url = "http://localhost:8000/v1/predictions/{}"
        # self.cancel_url = "http://localhost:8000/v1/predictions/{}/cancel"

        # Production
        self.predict_url = "https://api.rockai.online/v1/predictions"
        self.get_url = "https://api.rockai.online/v1/predictions/{}"
        self.cancel_url = "https://api.rockai.online/v1/predictions/{}/cancel"

    # Get a prediction result by ID
    def get(self, id: str):
        headers = {"Authorization": f"Bearer {self.api_token}"}
        response = requests.get(self.get_url.format(id), headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        result = response.json()
        logging.info(result)
        return result

    # Get a prediction result by ID (async)
    async def get_async(self, id: str):
        headers = {"Authorization": f"Bearer {self.api_token}"}

        async with aiohttp.ClientSession() as session:
            async with session.get(
                self.get_url.format(id), headers=headers
            ) as response:
                response.raise_for_status()  # Raise an exception for HTTP errors
                result = await response.json()
                logging.info(result)
                return result

    # Cancel a prediction by ID
    def cancel(self, id: str):
        headers = {"Authorization": f"Bearer {self.api_token}"}
        response = requests.post(self.cancel_url.format(id), headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        result = response.json()
        logging.info(result)
        return result

    # Cancel a prediction by ID (async)
    async def cancel_async(self, id: str):
        headers = {"Authorization": f"Bearer {self.api_token}"}
        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.cancel_url.format(id), headers=headers
            ) as response:
                response.raise_for_status()  # Raise an exception for HTTP errors
                result = await response.json()
                logging.info(result)
                return result

    # Stream output from a model, if model supports streaming like LLama3
    def stream(self, version: str, input: Optional[Dict[str, Any]] = None) -> Iterator:
        url = self.predict_url

        payload = {"version": version, "input": input, "stream": True}

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(self.api_token),
        }

        response = requests.post(url=url, headers=headers, json=payload)
        response.raise_for_status()
        create_result = response.json()
        if (
            response.status_code == 200
            or response.status_code == 201
            and "stream" in create_result["data"]["urls"]
        ):
            headers["Accept"] = "text/event-stream"
            headers["Cache-Control"] = "no-store"

            with httpx.Client() as client:
                with connect_sse(
                    client, create_result["data"]["urls"]["stream"]
                ) as event_source:
                    try:
                        for sse in event_source.iter_sse():
                            yield sse.data
                    except Exception as e:
                        logging.error(str(e))

    # Run a model and return the result from the model
    def run(
        self,
        version: str,
        input: Optional[Dict[str, Any]] = None,
        webhook: Optional[str] = None,
        webhook_events_filter: Optional[List[str]] = None,
    ) -> Any:
        url = self.predict_url

        payload = {"version": version, "input": input}
        if webhook is not None:
            payload["webhook"] = webhook
        if webhook_events_filter is not None:
            payload["webhook_events_filter"] = webhook_events_filter

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(self.api_token),
        }

        response = requests.post(url=url, headers=headers, json=payload)
        response.raise_for_status()
        create_result = response.json()
        if response.status_code == 200 or response.status_code == 201:
            while True:
                get_resp = requests.get(
                    url=self.get_url.format(create_result["data"]["id"]),
                    headers=headers,
                )
                get_resp.raise_for_status()
                get_result = get_resp.json()
                if (
                    get_result["data"]["status"] == "processing"
                    or get_result["data"]["status"] == "starting"
                ):
                    time.sleep(1)
                    continue
                else:
                    return get_result

    # Stream output from a model, if model supports streaming like LLama3 (async version)
    async def stream_async(self, version: str, input: Optional[Dict[str, Any]] = None):
        url = self.predict_url

        payload = {"version": version, "input": input, "stream": True}

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(self.api_token),
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(url=url, headers=headers, json=payload)
            response.raise_for_status()
            create_result = response.json()
            if "stream" in create_result["data"]["urls"]:

                logging.info(create_result["data"]["urls"])
                async with sse_client.EventSource(
                    create_result["data"]["urls"]["stream"]
                ) as event_source:

                    async for event in event_source:
                        yield event.data
                        if event.type == "done" and event.message == "done":
                            return
    # Run a model and return the result from the model (Async version)
    async def run_async(
        self,
        version: str,
        input: Optional[Dict[str, Any]] = None,
        webhook: Optional[str] = None,
        webhook_events_filter: Optional[List[str]] = None,
    ):
        url = self.predict_url

        payload = {"version": version, "input": input}
        if webhook is not None:
            payload["webhook"] = webhook
        if webhook_events_filter is not None:
            payload["webhook_events_filter"] = webhook_events_filter

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(self.api_token),
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(url=url, headers=headers, json=payload)
            response.raise_for_status()
            create_result = response.json()
            while True:
                get_resp = await client.get(
                    url=self.get_url.format(create_result["data"]["id"]),
                    headers=headers,
                )
                get_result = get_resp.json()
                if (
                    get_result["data"]["status"] == "processing"
                    or get_result["data"]["status"] == "starting"
                ):
                    await asyncio.sleep(1)
                    continue
                else:
                    return get_result