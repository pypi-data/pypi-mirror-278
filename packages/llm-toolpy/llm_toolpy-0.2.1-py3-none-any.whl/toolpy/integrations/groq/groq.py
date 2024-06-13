import time
import enum
import os
from typing import Optional, Dict, List, Tuple

import groq

from toolpy.llm import LLMInterface, Role

class GroqModel(enum.Enum):
    LLAMA3_70B = "llama3-70b-8192"

class GroqInterface(LLMInterface):
    _client : groq.Groq = None 

    def __init__(self, model:Optional[GroqModel] = None, n_retry:int = 0, api_key:Optional[str] = None) -> None:
        super().__init__(True, False, n_retry)

        if GroqInterface._client is None:

            if api_key is None:
                api_key = os.environ.get("GROQ_API_KEY")

            if api_key is None:
                raise RuntimeError("API key is not in the environment variables ('GROQ_API_KEY' variable is not set).")

            GroqInterface._client = groq.Groq(api_key=api_key)

        if model is None:
            model = GroqModel.LLAMA3_70B

        self._model = model.value

    def query(self, prompt: List[Tuple[Role, str]], json_mode: bool) -> str:
        messages = []
        for p in prompt:
            if p[0] == Role.SYSTEM:
                role = "system"
            else:
                role = "user"

            message = {"role":role, "content":p[1]}
            messages.append(message)

        response_format = None
        if json_mode:
            response_format = {"type": "json_object"}

        chat_completion = None
        while chat_completion is None:
            try:
                chat_completion = GroqInterface._client.chat.completions.create(
                                messages=messages,
                                model=self._model,
                                response_format=response_format
                            )
                
            except groq.RateLimitError as _:
                time.sleep(2)
        
        return chat_completion.choices[0].message.content