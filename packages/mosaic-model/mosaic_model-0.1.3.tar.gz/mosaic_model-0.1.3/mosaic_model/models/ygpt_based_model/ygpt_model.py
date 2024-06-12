import re
from typing import List

import requests

from mosaic_model.models.base_extractor import BaseExtractor


class YandexGPTTagger(BaseExtractor):
    def __init__(
        self,
        API_KEY: str,
        catalog_id: str,
    ) -> None:
        self.url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Api-Key {API_KEY}",
        }
        self.catalog_id = catalog_id

    def extract(self, text: str, top_n: int) -> List[str]:
        summarization = self.sumarization(text)
        tags = self.tagger(summarization, top_n)

        return tags

    def tagger(self, text: str, top_n: int) -> List[str]:
        response = requests.post(
            self.url,
            headers=self.headers,
            json=self._get_tagger_prompt(text, top_n=top_n),
        )
        tags = self._get_tags_from_response(response)
        return tags

    def sumarization(self, text: str) -> str:
        response = requests.post(
            self.url, headers=self.headers, json=self._get_summarization_prompt(text)
        )
        text = response.json()["result"]["alternatives"][0]["message"]["text"]
        return text

    @staticmethod
    def _get_tags_from_response(response) -> List[str]:
        text = response.json()["result"]["alternatives"][0]["message"]["text"]
        tags = re.findall("\[(.*?)\]", text)
        tags = [tag.lower() for tag in tags]

        return tags

    def _get_summarization_prompt(self, text: str) -> dict:
        prompt = {
            "modelUri": f"gpt://{self.catalog_id}/summarization/latest",
            "completionOptions": {
                "stream": False,
                "temperature": 0.2,
                "maxTokens": "2000",
            },
            "messages": [
                {
                    "role": "system",
                    "text": ("Ты - чат-бот, который сокращает тексты."),
                },
                {
                    "role": "user",
                    "text": f"Сократи следующий текст до одного абзаца: {text}.",
                },
            ],
        }

        return prompt

    def _get_tagger_prompt(self, text: str, top_n: int) -> dict:
        prompt = {
            "modelUri": f"gpt://{self.catalog_id}/yandexgpt/latest",
            "completionOptions": {
                "stream": False,
                "temperature": 0.2,
                "maxTokens": "2000",
            },
            "messages": [
                {
                    "role": "system",
                    "text": (
                        "Ты - чат-бот, который размечает тексты тегами на основе их содержания. "
                        f"Напиши {top_n} различных слов, которые характеризуют текст."
                    ),
                },
                {
                    "role": "user",
                    "text": f"{text}. Ответ дай в таком формате: [тег 1] [тег 2] [тег 3]",
                },
            ],
        }

        return prompt
