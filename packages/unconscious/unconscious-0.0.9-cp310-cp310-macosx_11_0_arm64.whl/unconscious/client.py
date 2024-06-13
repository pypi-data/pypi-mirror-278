import requests
from sseclient import SSEClient
import json
import json
import random
import time


def to_snake_case(name):
    """Converts CamelCase to snake_case."""
    return "".join(["_" + i.lower() if i.isupper() else i for i in name]).lstrip("_")


class BaseMessage:
    name: str

    @classmethod
    def from_dict(cls, json_data):
        # Find the correct subclass based on the json_data keys
        for subclass in cls.__subclasses__():
            if subclass.name in json_data:
                instance = subclass()
                for key, value in json_data[subclass.name].items():
                    setattr(instance, key, value)
                return instance
        raise ValueError("Invalid message type")

    def to_dict(self):
        return {self.name: self.__dict__}

    def is_type(self, wrapped_message_class):
        return self.name == wrapped_message_class.name


def msg(cls):
    class WrappedMessage(cls, BaseMessage):
        name = to_snake_case(cls.__name__)

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

    WrappedMessage.__name__ = cls.__name__
    return WrappedMessage


class UnconsciousClient:
    def __init__(
        self,
        thread="main",
        url="http://localhost:3000",
        base_inference_url="http://100.66.125.3:8080",
    ):
        self.thread = thread
        self.url = url
        self.base_inference_url = base_inference_url
        self.client = None
        unique_id = random.randint(0, 1000)
        self.unique_id = unique_id

    def connect(self, start_point_in_time=None):
        params = {}
        if start_point_in_time:
            params["start"] = start_point_in_time
        if self.thread:
            params["thread"] = self.thread
        response = requests.get(self.url + "/sse", stream=True, params=params)
        if response.status_code != 200:
            print("Failed to connect to SSE endpoint")
            return False
        self.client = SSEClient(response)
        return True

    def add_message(self, message):
        params = {}
        if self.thread:
            params["thread"] = self.thread
        response = requests.post(self.url + "/add", json=message, params=params)
        if response.status_code == 200:
            pass
        else:
            print(f"Failed to add message: {response} original message: {message}")
        return response

    def get_messages(self, start=None, end=None):
        params = {}
        if start:
            params["start"] = start
        if end:
            params["end"] = end
        response = requests.get(self.url + "/get", params=params)
        json_data = response.json()

        if isinstance(json_data, list):
            return [json.loads(proposal) for proposal in json_data]

        return json_data

    def listen(self, on_message=None):
        if not self.client:
            print("Not connected to any SSE endpoint.")
            return
        try:
            for msg in self.client.events():
                time.sleep(0.05)
                if on_message:
                    try:
                        # print(f"Received message: {msg.data}")
                        parsed_msg = json.loads(msg.data)
                        internal_msg = parsed_msg.get("message")
                        client_id = parsed_msg.get("client_id")
                        parsed_msg = json.loads(internal_msg)
                        wrapped_message = BaseMessage.from_dict(parsed_msg)
                        on_message(wrapped_message, client_id)
                    except Exception as e:
                        print(f"{self.unique_id} Error while parsing message: {e}")
                # do nothing if no on_message callback is provided
        except Exception as e:
            print(f"Error while listening to SSE events: {e}")
