import requests


class GoogleTranslateClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.url = (
            "https://google-translate1.p.rapidapi.com/language/translate/v2"
        )
        self.headers = {
            "content-type": "application/x-www-form-urlencoded",
            "Accept-Encoding": "application/gzip",
            "X-RapidAPI-Host": "google-translate1.p.rapidapi.com",
            "X-RapidAPI-Key": self.api_key
        }

    def translate_text(self, text, target_language, source_language='en'):
        data = {
            "q": text,
            "target": target_language,
            "source": source_language
        }

        response = requests.post(
            self.url,
            headers=self.headers,
            data=data
        )

        if response.status_code != 200:
            raise Exception(
                f"Error: {response.status_code}, {response.text.strip()}"
            )

        return response.json()
