import os

from dotenv import load_dotenv
from groq import (
    APIConnectionError,
    APIError,
    APITimeoutError,
    Groq,
    RateLimitError,
)

load_dotenv()

DEFAULT_MODEL = 'llama-3.3-70b-versatile'
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 1000


class AIClient:
    """AI Client for Groq integration"""

    def __init__(self):
        self.api_key = os.getenv('GROQ_API_KEY')
        if not self.api_key:
            raise RuntimeError('GROQ_API_KEY is not set. Copy .env.example to .env and add your Groq key.')

        self.client = Groq(api_key=self.api_key)
        self.model = os.getenv('GROQ_MODEL', DEFAULT_MODEL)

    def query(
        self,
        prompt: str,
        system_prompt: str | None = None,
        temperature: float = DEFAULT_TEMPERATURE,
        max_tokens: int = DEFAULT_MAX_TOKENS,
    ) -> str:
        """
        Send a prompt to Groq and get a response

        Args:
            prompt: The prompt to send
            system_prompt: System prompt for context
            temperature: Sampling temperature
            max_tokens: Maximum tokens in response

        Returns:
            AI response as string
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        'role': 'system',
                        'content': system_prompt or 'You are a helpful assistant for test automation.'
                    },
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ],
                temperature=temperature,
                max_tokens=max_tokens,
            )

            content = response.choices[0].message.content
            if content:
                return content.strip()
            return ''
        except (APIConnectionError, APITimeoutError, RateLimitError, APIError) as exc:
            print(f'AI Client Error: {exc!s}')
            raise RuntimeError(f'Groq API request failed: {exc!s}') from exc
