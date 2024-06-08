# placid_image_generator/generator.py

import requests
import json
import time

class PlacidImageGenerator:
    def __init__(self, api_key, template_uuid):
        self.api_key = api_key
        self.template_uuid = template_uuid
        self.api_url = "https://api.placid.app/api/rest/images"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def generate_image(self, img_url, headline_text, filename):
        data = {
            "template_uuid": self.template_uuid,
            "layers": {
                "img": {
                    "image": img_url
                },
                "headline": {
                    "text": headline_text
                }
            },
            "modifications": {
                "filename": filename
            }
        }

        response = requests.post(self.api_url, headers=self.headers, data=json.dumps(data))

        if response.status_code == 200:
            response_data = response.json()
            polling_url = response_data.get("polling_url")
            return self._poll_for_result(polling_url)
        else:
            raise Exception(f"Image generation failed: {response.status_code}, {response.text}")

    def _poll_for_result(self, polling_url):
        while True:
            poll_response = requests.get(polling_url, headers=self.headers)
            if poll_response.status_code == 200:
                poll_data = poll_response.json()
                if poll_data.get("status") == "finished":
                    return poll_data.get("image_url")
                elif poll_data.get("status") == "error":
                    raise Exception(f"Image generation error: {poll_data}")
                else:
                    print("이미지 생성 상태:", poll_data.get("status"))
            else:
                raise Exception(f"Polling failed: {poll_response.status_code}, {poll_response.text}")
            time.sleep(5)  # 5초 대기 후 다시 확인
