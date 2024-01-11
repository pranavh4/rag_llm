import os

from llama_index import VectorStoreIndex
from llama_index.chat_engine import ContextChatEngine
from llama_index.chat_engine.types import BaseChatEngine, ChatMode
from llama_index.core.llms.types import ChatMessage, MessageRole
from llama_index.schema import Document

from .ft_scraper import get_articles
from .utils import load_config_file

config = load_config_file()
os.environ["OPENAI_API_KEY"] = config["openai_api_key"]


class RetrievalClassifier:
    def __init__(self):
        self.prompt_template: str = load_config_file()['retrieval_classifier']['prompt_template']
        self.index = VectorStoreIndex.from_documents([])
        self.chat_engine = self.index.as_chat_engine(chat_mode=ChatMode.SIMPLE)

    def requires_retrieval(self, query: str, response: str) -> bool:
        prompt = self.prompt_template.format(query, response)
        response = str(self.chat_engine.chat(prompt))
        print(response)
        return not response.lower().startswith("yes")


class RagLLM:
    def __init__(self, retrieval_classifier: RetrievalClassifier):
        self.retrieval_classifier = retrieval_classifier
        self.index: VectorStoreIndex = VectorStoreIndex.from_documents([])
        self.chat_history: list[ChatMessage] = []
        self.retriever = self.index.as_retriever()
        self.chat_engine = self._create_chat_engine()

    def update_index(self, query: str):
        articles = get_articles(query)

        for article in articles:
            self.index.insert(Document(text=article))

        self.chat_engine = self._create_chat_engine()

    def get_response(self, query: str) -> str:
        response_txt = str(self.chat_engine.chat(query))
        print(response_txt)

        if self.retrieval_classifier.requires_retrieval(query, response_txt):
            self.update_index(query)
            response_txt = str(self.chat_engine.chat(query))

        user_message = ChatMessage(
            role=MessageRole.USER,
            content=query,
        )
        response_message = ChatMessage(
            role=MessageRole.ASSISTANT,
            content=response_txt
        )
        self.chat_history.extend([user_message, response_message])

        return response_txt

    def _create_chat_engine(self) -> BaseChatEngine:
        chat_engine = ContextChatEngine.from_defaults(
            retriever=self.index.as_retriever(),
            chat_history=self.chat_history,
            verbose=True,
        )

        return chat_engine
