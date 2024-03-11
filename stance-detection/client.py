import requests
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class Client:
    def __init__(self) -> None:
        self.session = requests.Session()
        self.llama_url = "http://localhost:11434"
        self.openai_api_key = os.environ.get("OPENAI_API_KEY")

        self.openai_client = OpenAI(
            # This is the default and can be omitted
            api_key=self.openai_api_key,
        )

    def get_response_llama(self, prompt: str, system: str) -> str:
        print(f"Prompt: {prompt}")
        print(f"System: {system}")
        response = self.session.post(
            f"{self.llama_url}/api/generate/",
            json={
                "model": "llama2",
                "prompt": prompt,
                "system": system,
                "stream": False,
                "format": "json",
            },
        )
        response.raise_for_status()
        return response.json()["response"]

    def get_response_gpt3(self, prompt: str, system: str) -> str | None:
        print(f"Prompt: {prompt}")
        print("=-=--=-=-=-=")

        response = self.openai_client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": system,
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            model="gpt-3.5-turbo",
            response_format={"type": "json_object"},
        )
        return response.choices[0].message.content
