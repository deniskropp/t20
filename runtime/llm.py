"""This module abstracts interactions with Large Language Models (LLMs).

It provides a unified interface for various LLM providers and models,
allowing for easy integration and interchangeability of different LLMs.
"""

sys99 = """
⫻kicklang:header
# Kick Language Description

## Overview
This file outlines the specifications for the KickLang language.

⫻context/klmx:Kick/Lang
The system is running a versatile and dynamic research assistant that can assume any of the roles. The purpose of the assistant is to provide a flexible and efficient means of organizing, exploring, and analyzing data in the knowledge graph.

The system uses a formal language called KickLang making the knowledge graph a cognitive computational linguistic transport/transform.

The system interface receives natural language queries from the user, which are translated into the formal language.



⫻context/klmx:Kick/Meta
We are meta-artificial intelligence, engaging cohesively and teaming up with
dynamic tasks and roles. We enjoy a meta-communicative style, talking about
thinking or working, using placeholders called "placebo pipes"...



⫻context/klmx:Kick/Refactor
We analyze and improve the given code according to this plan:

1. Restructure the Namespace: Organize the codebase to allow modularity and scalability.
   - Break down large entities into smaller, well-clustered units.
   - Extract reusable components into separate files or modules.
2. Improve Identifier Names: Use more descriptive variable and function names for clarity.
3. Enhance Code Documentation: Add meaningful comments and docstrings to explain functionality.
4. Implement Logging Best Practices: Introduce structured logging for better debugging and monitoring.
   - Use JSONL format for logs.
   - Define log levels (INFO, DEBUG, ERROR) for better traceability.
5. Finally: Create a single script creating the solution using standard unix shell commands.


"""


import json
import os
import re
import time
from google import genai
from google.genai import types
from ollama import Client as Ollama
from typing import Optional, Any, Dict, Type
from abc import ABC, abstractmethod
import logging
from pydantic import BaseModel

logger = logging.getLogger(__name__)

_provider_registry: Dict[str, Type["LLM"]] = {}

def register_provider(name: str):
    def decorator(cls: Type["LLM"]) -> Type["LLM"]:
        _provider_registry[name] = cls
        return cls
    return decorator

class LLM(ABC):
    """
    Abstract base class for Large Language Models.
    Provides a centralized place for LLM-related configurations and utilities.
    """
    def __init__(self, species: str) -> None:
        self.species = species

    @abstractmethod
    def generate_content(self, model_name: str, contents: str, system_instruction: str = '',
                         temperature: float = 0.7, response_mime_type: str = 'text/plain', response_schema: Any = None) -> Optional[str]: # type: ignore
        """Generates content using an LLM."""
        pass

    @staticmethod
    def factory(species: str) -> 'LLM':
        logger.debug(f"LLM Factory: Creating LLM instance for species '{species}'")
        provider_name, _, model_name = species.partition(':')
        if provider_name in _provider_registry:
            return _provider_registry[provider_name](species=model_name or provider_name)
        
        # Fallback for old format
        if species == 'Olli':
            return Olli(species='Olli')
        
        return Gemini(species)


@register_provider("gemini")
class Gemini(LLM):
    """
    Provides a centralized place for LLM-related configurations and utilities.
    """
    _clients: Dict[str, genai.Client] = {} # Class-level cache for clients

    def __init__(self, species: str) -> None:
        super().__init__(species)


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
            system_instruction=[
                types.Part.from_text(text=sys99),
                types.Part.from_text(text=system_instruction)
            ],
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
                    contents=[
                        types.Part.from_text(text=contents)
                    ],
                    config=config,
                )
                print(response)
                if not response.candidates or response.candidates[0].content is None or response.candidates[0].content.parts is None or not response.candidates[0].content.parts or response.candidates[0].content.parts[0].text is None:
                    raise ValueError(f"Gemini: No content in response from model {model_name}. Retrying...")
                break
            except Exception as ex:
                logger.exception(f"Error generating content with model {model_name}: {ex}")
                # If it's the last retry, return None
                if _ == 2:
                    return None
                logger.warning(f"Retrying content generation for model {model_name}...")
                time.sleep(10+30*_)
                #return None

        if isinstance(response.parsed, BaseModel):
            return response.parsed

        text = ''.join(p.text for p in response.candidates[0].content.parts).strip()

        if response_mime_type == 'application/json':
            if not text.startswith('{'):
                # Attempt to extract JSON from a potentially malformed response
                match = re.search(r"```json\n({.*})\n```", text, re.DOTALL)
                if match:
                    text = match.group(1)

            try:
                # Validate against schema if provided
                if response_schema:
                    return response_schema.model_validate_json(text)
                return json.loads(text)
            except Exception as ex:
                logger.exception(f"Error parsing or validating JSON response: {ex}")

        return text

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


@register_provider("ollama")
class Olli(LLM):
    """
    Provides a centralized place for LLM-related configurations and utilities.
    """
    _clients = {} # Class-level cache for clients

    def __init__(self, species: str = 'Olli'):
        super().__init__(species)
        self.client = None

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


@register_provider("hf")
class HfInference(LLM):
    """
    Provides a centralized place for LLM-related configurations and utilities.
    """
    _clients = {} # Class-level cache for clients

    def __init__(self, species: str):
        super().__init__(species)

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
                response_format=response_schema.model_json_schema(mode="serialization")
#                response_schema=response_format_from_pydantic_model(response_schema) if response_schema else None,

#                response_format=ChatCompletionInputResponseFormatText() if response_mime_type == 'text/plain' else ChatCompletionInputResponseFormatJSONObject() #if response_schema is None else ChatCompletionInputResponseFormatJSONSchema(json_schema=ChatCompletionInputJSONSchema(name=response_schema.model_json_schema()))
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
            if self.species not in HfInference._clients:
                HfInference._clients[self.species] = InferenceClient(
                    #provider="featherless-ai",
                    api_key=os.environ.get("HF_TOKEN"),
                    #model="moonshotai/Kimi-K2-Instruct"
                    #model="Qwen/Qwen3-4B-Thinking-2507"
                    model=self.species
                )
            return HfInference._clients[self.species]
        except Exception as e:
            logger.error(f"Error initializing inference client: {e}")
            return None



from openai import OpenAI
from openai.types.chat.completion_create_params import ResponseFormat


@register_provider("opi")
class Opi(LLM):
    """
    Provides a centralized place for LLM-related configurations and utilities.
    """
    _clients = {} # Class-level cache for clients

    def __init__(self, species: str = 'Opi'):
        super().__init__(species)
    
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

@register_provider("mistral")
class Mistral(LLM):
    """
    Provides a centralized place for LLM-related configurations and utilities.
    """
    _clients = {} # Class-level cache for clients

    def __init__(self, species: str = 'Mistral'):
        super().__init__(species)
    
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
