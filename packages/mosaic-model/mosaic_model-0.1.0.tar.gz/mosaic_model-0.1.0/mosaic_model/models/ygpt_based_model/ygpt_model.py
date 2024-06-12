import re
from typing import List

import requests


class YandexGPTTagger:
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

    def tag(self, text: str) -> List[str]:
        summarization = self.sumarization(text)
        response = requests.post(
            self.url,
            headers=self.headers,
            json=self._get_request_json(summarization, summarization=False),
        )
        tags = self._get_tags_from_response(response)
        return tags

    def sumarization(self, text: str) -> str:
        response = requests.post(
            self.url, headers=self.headers, json=self._get_request_json(text, summarization=True)
        )
        text = response.json()["result"]["alternatives"][0]["message"]["text"]
        return text

    @staticmethod
    def _get_tags_from_response(response) -> List[str]:
        text = response.json()["result"]["alternatives"][0]["message"]["text"]
        print(text)
        tags = re.findall("\[(.*?)\]", text)
        tags = [tag.lower() for tag in tags]

        return tags

    def _get_request_json(self, text: str, summarization: bool) -> dict:
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
                        "Напиши не более трех различных слов, которые характеризуют текст."
                    ),
                },
                {
                    "role": "user",
                    "text": f"{text}. Ответ дай в таком формате: [тег 1] [тег 2] [тег 3]",
                },
            ],
        }

        if summarization:
            prompt["modelUri"] = f"gpt://{self.catalog_id}/summarization/latest"

        return prompt
