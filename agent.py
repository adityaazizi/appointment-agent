import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from fastapi import HTTPException

load_dotenv()


class Agent:
    def __init__(self):
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def get_openai_response(self, messages):
        response = self.openai_client.chat.completions.create(
            model='gpt-4o-mini',
            messages=messages
        )
        return response.choices[0].message.content
