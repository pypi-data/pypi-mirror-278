import base64
import hashlib
import json
from typing import List

from langchain_core.embeddings.embeddings import Embeddings
from langchain_openai import OpenAIEmbeddings
from redis import Redis


def hash_string_base64(s, max_length=100):
    # Hash the string using SHA-256
    hash_object = hashlib.sha256(s.encode())
    hash_bytes = hash_object.digest()  # Get the hash as bytes

    # Encode the hash in base64
    hash_base64 = base64.b64encode(hash_bytes).decode("utf-8")

    # Truncate or somehow reduce the size to meet max_length requirement
    # Note: You might want to adjust the logic to ensure the final string meets your exact requirements
    truncated_hash = hash_base64[:max_length]

    return truncated_hash


class RedisCachedOpenAIEmbeddings(Embeddings):
    def __init__(self, redis_client: Redis):
        self.redis_client = redis_client
        self.openai_client = OpenAIEmbeddings()

    @staticmethod
    def _get_key(text):
        return f"llm-embeddings-openai-{hash_string_base64(text)}"

    def _get_from_cache(self, text) -> list[float] | None:
        value = self.redis_client.get(self._get_key(text))
        if value is None:
            return None
        return json.loads(value)

    def _set_in_cache(self, text, value):
        self.redis_client.set(self._get_key(text), json.dumps(value))

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        # get cached values
        cached_documents = {text: self._get_from_cache(text) for text in texts}
        # embed new values
        uncached_texts = [text for text in texts if cached_documents.get(text) is None]
        documents = self.openai_client.embed_documents(uncached_texts)
        # add to cache
        new_documents = {}
        for text, document in zip(uncached_texts, documents):
            self._set_in_cache(text, document)
            new_documents[text] = document

        # return all values in the same order
        return [
            cached_documents.get(text)
            if cached_documents.get(text) is not None
            else new_documents.get(text)
            for text in texts
        ]

    def embed_query(self, text: str) -> List[float]:
        # get cached value
        cached_value = self._get_from_cache(text)
        if cached_value is not None:
            return cached_value
        # embed new value
        document = self.openai_client.embed_query(text)
        # add to cache
        self._set_in_cache(text, document)
        return document
