import json
import os
from typing import List

from crisper_api_client import AuthenticatedClient
from crisper_api_client.api.api import api_v1_assistant_list, api_v1_assistant_retrieve, api_v1_assistant_create
from crisper_api_client.models import Assistant

CRISPER_TOKEN = os.getenv("CRISPER_TOKEN", None)
IS_DEV = os.getenv("ENV", "production") == "development"

class Crisper:
    def __init__(self):
        if not CRISPER_TOKEN:
            raise ValueError("CRISPER_TOKEN is required in the environment variables.")
        base_url = "http://localhost:8000" if IS_DEV else "https://api.crisper.ai"
        self.client = AuthenticatedClient(token=CRISPER_TOKEN, base_url=base_url)
        from crisper_api_client.serivces.assistant_service import AssistantService
        AssistantService.client = self.client

    def assistants(self) -> List[Assistant]:
        response = api_v1_assistant_list.sync_detailed(client=self.client)
        return response.parsed.results

    def get_assistant(self, name: str):
        response = api_v1_assistant_retrieve.sync_detailed(name, client=self.client)
        if response.status_code == 200:
            return Assistant.from_dict(json.loads(response.content))
        return None

    def _create_assistant(self, name: str):
        assistant = Assistant(name=name, knowledge_sources=[])
        response = api_v1_assistant_create.sync_detailed(body=assistant, client=self.client)
        to_return = None
        if response.status_code == 201:
            return Assistant.from_dict(json.loads(response.content))
        return to_return


    @staticmethod
    def create_assistant(name: str):
        crisper = Crisper()
        return crisper._create_assistant(name)