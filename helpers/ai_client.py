import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


class AIClient:
    """AI Client for Groq integration"""
    
    def __init__(self):
        self.client = Groq(api_key=os.getenv('GROQ_API_KEY'))
        self.model = os.getenv('GROQ_MODEL', 'llama-3.3-70b-versatile')
    
    def query(self, prompt: str, system_prompt: str = None, temperature: float = 0.7, max_tokens: int = 1000) -> str:
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
                max_tokens=max_tokens
            )
            
            content = response.choices[0].message.content
            if content:
                return content.strip()
            return ''
        except Exception as e:
            print(f'AI Client Error: {str(e)}')
            raise
