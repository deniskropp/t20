import os
from google import genai
from google.genai import types
from ollama import Client as Ollama
from typing import Optional, Any
from abc import ABC, abstractmethod
import logging
from pydantic import BaseModel


logger = logging.getLogger(__name__)


class LLM(ABC):
    """
    Abstract base class for Large Language Models.
    Provides a centralized place for LLM-related configurations and utilities.
    """
    def __init__(self):
        pass

    @abstractmethod
    def generate_content(self, model_name: str, contents: str, system_instruction: str = '',
                         temperature: float = 0.7, response_mime_type: str = 'text/plain', response_schema: BaseModel | None = None) -> Optional[str]:
        """Generates content using an LLM."""
        pass

    @staticmethod
    def factory(role_name: str = '') -> 'LLM':
        if role_name == 'Olli':
            return Olli()
        elif role_name == 'Kimi':
            return Kimi()
        #else:
        # TODO: Make this configurable, e.g., from runtime.yaml or an environment variable.
        return Gemini()


class Gemini(LLM):
    """
    Provides a centralized place for LLM-related configurations and utilities.
    """
    def __init__(self):
        self.client = None

    def generate_content(self, model_name: str, contents: str, system_instruction: str = '',
                         temperature: float = 0.7, response_mime_type: str = 'text/plain', response_schema: Any = None) -> Optional[str]:
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
            if not response.candidates or response.candidates[0].content is None or response.candidates[0].content.parts is None or not response.candidates[0].content.parts or response.candidates[0].content.parts[0].text is None:
                return None
            if response_mime_type == 'application/json':
                try:
                    # Attempt to parse the JSON response
                    json_output = response.candidates[0].content.parts[0].text.strip()
                    # Validate against schema if provided
                    if response_schema:
                        response_schema.model_validate_json(json_output)
                    return json_output
                except Exception as json_e:
                    logger.error(f"Error parsing or validating JSON response: {json_e}")
                    # Optionally, return the raw text if JSON parsing fails but you still want to see it
                    return response.candidates[0].content.parts[0].text.strip()
                    
            return response.candidates[0].content.parts[0].text.strip()
        except Exception as e:
            logger.error(f"Error generating content with model {model_name}: {e}")
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
            logger.error(f"Error initializing GenAI client: {e}")
            return None


class Olli(LLM):
    """
    Provides a centralized place for LLM-related configurations and utilities.
    """
    def __init__(self):
        self.client = None

    def generate_content(self, model_name: str, contents: str, system_instruction: str = '',
                         temperature: float = 0.7, response_mime_type: str = 'text/plain', response_schema: Any = None) -> Optional[str]:
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
            logger.error(f"Error generating content with model {model_name}: {e}")
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
            logger.error(f"Error initializing GenAI client: {e}")
            return None






from huggingface_hub import InferenceClient, ChatCompletionInputResponseFormatText, ChatCompletionInputResponseFormatJSONObject, ChatCompletionInputResponseFormatJSONSchema, ChatCompletionInputJSONSchema


class Kimi(LLM):
    """
    Provides a centralized place for LLM-related configurations and utilities.
    """
    def __init__(self):
        self.client = None

    def generate_content(self, model_name: str, contents: str, system_instruction: str = '',
                         temperature: float = 0.7, response_mime_type: str = 'text/plain', response_schema: BaseModel | None = None) -> Optional[str]:
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
            out = ""

            stream = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": system_instruction
                    },
                    {
                        "role": "user",
                        "content": contents
                    },
                ],
                temperature=temperature,
                max_tokens=50000,
                top_p=1,
                stream=True,
                response_format=ChatCompletionInputResponseFormatText() if response_mime_type == 'text/plain' else ChatCompletionInputResponseFormatJSONObject() #if response_schema is None else ChatCompletionInputResponseFormatJSONSchema(json_schema=ChatCompletionInputJSONSchema(name=response_schema.model_json_schema()))
            )

            for chunk in stream:
                if chunk.choices[0].delta.content is None:
                    continue
                print(chunk.choices[0].delta.content, end="")
                out += chunk.choices[0].delta.content

            return out
        except Exception as e:
            logger.error(f"Error generating content with model {model_name}: {e}")
            return None

    def _get_client(self):
        """
        Returns a inference client instance.
        """
        try:
            if (self.client is None):
                self.client = client = InferenceClient(
                    provider="featherless-ai",
                    api_key=os.environ.get("HF_TOKEN"),
                    model="moonshotai/Kimi-K2-Instruct"
                )
            return self.client
        except Exception as e:
            logger.error(f"Error initializing GenAI client: {e}")
            return None
