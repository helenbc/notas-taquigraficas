import requests


class Client:
    def __init__(self) -> None:
        self.session = requests.Session()
        self.url = "http://localhost:11434"

    def get_response(self, prompt: str, system: str) -> str:
        print(f"Prompt: {prompt}")
        print(f"System: {system}")
        response = self.session.post(
            f"{self.url}/api/generate/",
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
