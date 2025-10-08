"""This module abstracts interactions with Large Language Models (LLMs).

It provides a unified interface for various LLM providers and models,
allowing for easy integration and interchangeability of different LLMs.
"""

import json
import os
import time
from google import genai
from google.genai import types
from ollama import Client as Ollama
from typing import Optional, Any, Dict
from abc import ABC, abstractmethod
import logging
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class LLM(ABC):
    """
    Abstract base class for Large Language Models.
    Provides a centralized place for LLM-related configurations and utilities.
    """
    def __init__(self) -> None:
        pass

    @abstractmethod
    def generate_content(self, model_name: str, contents: str, system_instruction: str = '',
                         temperature: float = 0.7, response_mime_type: str = 'text/plain', response_schema: Any = None) -> Optional[str]: # type: ignore
        """Generates content using an LLM."""
        pass

    @staticmethod
    def factory(species: str) -> 'LLM':
        print(f"LLM Factory: Creating LLM instance for species '{species}'")
        if species == 'Olli':
            return Olli()
        elif species == 'Kimi':
            return Kimi()
        if species.startswith('ollama:'):
            # Extract model name after 'ollama:'
            model_name = species.split(':', 1)[1]
            return Olli(species=model_name)
        if species.startswith('opi:'):
            # Extract model name after 'opi:'
            model_name = species.split(':', 1)[1]
            return Opi(species=model_name)
        if species.startswith('mistral:'):
            # Extract model name after 'mistral:'
            model_name = species.split(':', 1)[1]
            return Mistral(species=model_name)
        return Gemini(species)


class Gemini(LLM):
    """
    Provides a centralized place for LLM-related configurations and utilities.
    """
    _clients: Dict[str, genai.Client] = {} # Class-level cache for clients

    def __init__(self, species: str) -> None:
        self.species = species

    def generate_content(self, model_name: str, contents: str, system_instruction: str = '',
                         temperature: float = 0.7, response_mime_type: str = 'text/plain', response_schema: BaseModel = None) -> Optional[str]: # type: ignore
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
            response_schema=response_schema,
            max_output_tokens=50000,
        )

        # try three times
        for _ in range(3):
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=contents,
                    config=config,
                )
                if not response.candidates or response.candidates[0].content is None or response.candidates[0].content.parts is None or not response.candidates[0].content.parts or response.candidates[0].content.parts[0].text is None:
                    raise ValueError(f"Gemini: No content in response from model {model_name}. Retrying...")
                break
            except Exception as ex:
                logger.exception(f"Error generating content with model {model_name}: {ex}")
                # If it's the last retry, return None
                if _ == 2:
                    return None
                logger.warning(f"Retrying content generation for model {model_name}...")
                time.sleep(10)
                #return None

        if isinstance(response.parsed, BaseModel):
            return response.parsed

        if response_mime_type == 'application/json':
            try:
                # Attempt to parse the JSON response
                json_output = response.candidates[0].content.parts[0].text.strip()
                # Validate against schema if provided
                if response_schema:
                    response_schema.model_validate_json(json_output)
                return json_output
            except Exception as ex:
                logger.exception(f"Error parsing or validating JSON response: {ex}")

        return response.candidates[0].content.parts[0].text.strip()

    def _get_client(self) -> genai.Client:
        """
        Returns a GenAI client instance.
        """
        try:
            if self.species not in Gemini._clients:
                logger.info(f"Initializing GenAI client for species {self.species}")
                Gemini._clients[self.species] = genai.Client()
            return Gemini._clients[self.species]
        except Exception as e:
            logger.exception(f"Error initializing GenAI client: {e}")
            raise


class Olli(LLM):
    """
    Provides a centralized place for LLM-related configurations and utilities.
    """
    _clients = {} # Class-level cache for clients

    def __init__(self, species: str = 'Olli'):
        self.client = None
        self.species = species

    def generate_content(self, model_name: str, contents: str, system_instruction: str = '',
                         temperature: float = 0.7, response_mime_type: str = 'text/plain', response_schema: BaseModel = None) -> Optional[str]: # type: ignore
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
        print(f"Olli: Using model {model_name} with temperature {temperature}")
        client = self._get_client(species=self.species)
        if not client:
            return None

        try:
            out = ""
            fmt = response_schema.model_json_schema(by_alias=False, mode='serialization')
            print(f"Olli: Using response format {fmt}")
            response = client.generate(
                model=self.species,#model_name,
                prompt=contents,
                format=fmt,
                options={"temperature": temperature, "system_instruction": system_instruction},
                stream=True
            )
            for chunk in response:
                if hasattr(chunk, "response") and chunk.response:
                    print(chunk.response, end="")
                    out += chunk.response
            return out
        except Exception as e:
            logger.error(f"Error generating content with model {model_name}: {e}")
            return None

    @staticmethod
    def _get_client(species: str):
        """
        Returns a GenAI client instance.
        """
        try:
            if (Olli._clients is None):
                Olli._clients = {}
            if species not in Olli._clients:
                Olli._clients[species] = Ollama()#base_url='http://localhost:11434')
            return Olli._clients[species]
        except Exception as e:
            logger.exception(f"Error initializing Ollama client: {e}")
            return None





from huggingface_hub import InferenceClient, ChatCompletionInputResponseFormatText, ChatCompletionInputResponseFormatJSONObject, ChatCompletionInputResponseFormatJSONSchema, ChatCompletionInputJSONSchema


class Kimi(LLM):
    """
    Provides a centralized place for LLM-related configurations and utilities.
    """
    _clients = {} # Class-level cache for clients

    def __init__(self, species: str = 'Kimi'):
        self.species = species
    
    def generate_content(self, model_name: str, contents: str, system_instruction: str = '',
                         temperature: float = 0.7, response_mime_type: str = 'text/plain', response_schema: BaseModel = None) -> Optional[str]: # type: ignore
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
                if self.species not in Kimi._clients:
                    Kimi._clients[self.species] = InferenceClient(
                        provider="featherless-ai",
                        api_key=os.environ.get("HF_TOKEN"),
                        model="moonshotai/Kimi-K2-Instruct"
                    )
            return Kimi._clients[self.species]
        except Exception as e:
            logger.error(f"Error initializing GenAI client: {e}")
            return None



from openai import OpenAI
from openai.types.chat.completion_create_params import ResponseFormat


class Opi(LLM):
    """
    Provides a centralized place for LLM-related configurations and utilities.
    """
    _clients = {} # Class-level cache for clients

    def __init__(self, species: str = 'Opi'):
        self.species = species
    
    def generate_content(self, model_name: str, contents: str, system_instruction: str = '',
                         temperature: float = 0.7, response_mime_type: str = 'text/plain', response_schema: BaseModel = None) -> Optional[str]: # type: ignore
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

            response_format: ResponseFormat = {"type": "text"}

            if response_mime_type == 'application/json':
                response_format = {"type": "json_object"}

            if response_schema:
                response_format = {"type": "json_schema", "json_schema": response_schema.model_json_schema()}   # type: ignore

            print(f"Opi: Using response format {response_format}")

            stream = client.chat.completions.create(
                model=model_name,
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
                response_format=response_format
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
        Returns a OpenAI client instance.
        """
        try:
            if (self.client is None):
                if self.species not in Opi._clients:
                    Opi._clients[self.species] = OpenAI(api_key=os.environ.get("OPENAI_API_KEY",""), base_url=os.environ.get("OPENAI_API_BASE"))
            return Opi._clients[self.species]
        except Exception as e:
            logger.error(f"Error initializing OpenAI client: {e}")
            return None



##


from mistralai import Mistral as MistralClient
from mistralai.extra.utils import response_format_from_pydantic_model

class Mistral(LLM):
    """
    Provides a centralized place for LLM-related configurations and utilities.
    """
    _clients = {} # Class-level cache for clients

    def __init__(self, species: str = 'Mistral'):
        self.species = species
    
    def generate_content(self, model_name: str, contents: str, system_instruction: str = '',
                         temperature: float = 0.7, response_mime_type: str = 'text/plain', response_schema: BaseModel = None) -> Optional[str]: # type: ignore
        """
        Generates content using the specified Mistral model.

        Args:
            model_name (str): The name of the model to use (e.g., "mistral-large-latest").
            contents (str): The input content for the model.
            system_instruction (str, optional): System-level instructions for the model.
            temperature (float, optional): Controls the randomness of the output. Defaults to 0.7.
            response_mime_type (str, optional): The desired MIME type for the response.
            response_schema (Any, optional): The schema for the response.

        Returns:
            str: The response from the Mistral model.
        """
        client = Mistral._get_client(species=self.species)
        if not client:
            return None
        try:
            messages = []
            if system_instruction:
                messages.append({"role": "system", "content": system_instruction})
            messages.append({"role": "user", "content": contents})

            print(f"Mistral: Using model {model_name} with temperature {temperature}")

            response_format = {"type": "text"}

            if response_mime_type == 'application/json':
                response_format = {"type": "json_object"}

            if response_schema:
                response_format = response_format_from_pydantic_model(response_schema)  # type: ignore


            out = ""
            stream = client.chat.stream(
                model=self.species,#model_name,
                messages=messages,
                temperature=temperature,
                max_tokens=50000,
                response_format=response_format # type: ignore
            )
            for chunk in stream:
                if chunk.data.choices[0].delta.content is None:
                    continue
                print(chunk.data.choices[0].delta.content, end="")
                out += str(chunk.data.choices[0].delta.content)

            return out
        except Exception as e:
            print(f"Error generating content with model {model_name}: {e}")
            return None

    @staticmethod
    def _get_client(species: str):
        """
        Returns a Mistral client instance.
        """
        try:
            if Mistral._clients is None:
                Mistral._clients = {}
            if species not in Mistral._clients:
                api_key = os.environ.get("MISTRAL_API_KEY")
                if not api_key:
                    raise ValueError("MISTRAL_API_KEY environment variable not set.")
                Mistral._clients[species] = MistralClient(api_key=api_key)
            return Mistral._clients[species]
        except Exception as e:
            logger.exception(f"Error initializing Mistral client: {e}")
            return None
