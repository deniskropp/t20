from google import genai
from google.genai import types
from ollama import Client as Ollama
from typing import Optional




class LLM:
    """
    Provides a centralized place for LLM-related configurations and utilities.
    """
    def __init__(self):
        pass

    def generate_content(self, model_name: str, contents: str, system_instruction: str = '',
                         temperature: float = 0.7, response_mime_type: str = 'text/plain', response_schema=None) -> Optional[str]:
        return None

    @staticmethod
    def factory() -> 'LLM':
        return Gemini()
        return Olli()


class Gemini(LLM):
    """
    Provides a centralized place for LLM-related configurations and utilities.
    """
    def __init__(self):
        self.client = None

    def generate_content(self, model_name: str, contents: str, system_instruction: str = '',
                         temperature: float = 0.7, response_mime_type: str = 'text/plain', response_schema=None) -> Optional[str]:
        """
        Generates content using the specified GenAI model.

        Args:
            model_name (str): The name of the model to use (e.g., "gemini-pro").
            contents (str): The input content for the model.
            system_instruction (str, optional): System-level instructions for the model.
            temperature (float, optional): Controls the randomness of the output. Defaults to 0.7.
            response_mime_type (str, optional): The desired MIME type for the response.
            response_schema (Any, optional): The schema for the response.

        Returns:
            types.GenerateContentResponse: The response from the GenAI model.
        """
        client = self._get_client()
        if not client:
            return None

        config = types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=temperature,
            response_mime_type=response_mime_type,
            response_schema=response_schema
        )

        try:
            response = client.models.generate_content(
                model=model_name,
                contents=contents,
                config=config,
            )
            return response.candidates[0].content.parts[0].text.strip()
        except Exception as e:
            print(f"Error generating content with model {model_name}: {e}")
            return None

    def _get_client(self):
        """
        Returns a GenAI client instance.
        """
        try:
            if (self.client is None):
                self.client = genai.Client()
            return self.client
        except Exception as e:
            print(f"Error initializing GenAI client: {e}")
            return None


class Olli(LLM):
    """
    Provides a centralized place for LLM-related configurations and utilities.
    """
    def __init__(self):
        self.client = None

    def generate_content(self, model_name: str, contents: str, system_instruction: str = '',
                         temperature: float = 0.7, response_mime_type: str = 'text/plain', response_schema=None) -> Optional[str]:
        """
        Generates content using the specified GenAI model.

        Args:
            model_name (str): The name of the model to use (e.g., "gemini-pro").
            contents (str): The input content for the model.
            system_instruction (str, optional): System-level instructions for the model.
            temperature (float, optional): Controls the randomness of the output. Defaults to 0.7.
            response_mime_type (str, optional): The desired MIME type for the response.
            response_schema (Any, optional): The schema for the response.

        Returns:
            types.GenerateContentResponse: The response from the GenAI model.
        """
        client = self._get_client()
        if not client:
            return None

        try:
            response = client.chat(model=model_name,
                                   messages=[{"role": "user", "content": contents}],
                                   options={"temperature": temperature, "system_instruction": system_instruction},
                                   stream=False)
            return response.message.content
        except Exception as e:
            print(f"Error generating content with model {model_name}: {e}")
            return None

    def _get_client(self):
        """
        Returns a GenAI client instance.
        """
        try:
            if (self.client is None):
                self.client = Ollama(base_url='http://localhost:11436')
            return self.client
        except Exception as e:
            print(f"Error initializing GenAI client: {e}")
            return None
