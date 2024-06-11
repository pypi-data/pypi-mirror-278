import json
import logging

from crisper_api_client import AuthenticatedClient
from crisper_api_client.api.api import api_v1_assistant_knowledge_source_create, api_v1_assistant_ask_create
from crisper_api_client.models import Assistant, KnowledgeSource, Question, Answer
from crisper_api_client.models.knowledge_source_content_type import KnowledgeSourceContentType


logger = logging.getLogger(__name__)

class AssistantService:
    client: AuthenticatedClient = None

    @classmethod
    def add_knowledge_source(cls, assistant, content_type: str, text: str = '', url: str = ''):
        knowledge_source = KnowledgeSource(
            content_type=KnowledgeSourceContentType(content_type),
            text=text,
            url=url,
        )
        response = api_v1_assistant_knowledge_source_create.sync_detailed(
            name=assistant.name,
            body=knowledge_source,
            client=cls.client
        )
        if response.status_code == 200:
            return Assistant.from_dict(json.loads(response.content))
        return None

    @classmethod
    def ask(cls, assistant, text: str):
        question = Question(text=text)
        response = api_v1_assistant_ask_create.sync_detailed(
            name=assistant.name,
            body=question,
            client=cls.client
        )
        if response.status_code == 200:
            return Answer.from_dict(json.loads(response.content))
        logger.error(f"Error: {response.status_code}")
        return None


Assistant.add_knowledge_source = lambda assistant, **kwargs: AssistantService.add_knowledge_source(assistant, **kwargs)
Assistant.ask = lambda assistant, text: AssistantService.ask(assistant, text)