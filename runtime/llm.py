"""This module abstracts interactions with Large Language Models (LLMs).

It provides a unified interface for various LLM providers and models,
allowing for easy integration and interchangeability of different LLMs.
"""


sys41 = """
⫻kicklang:header
# Section Format Description

⫻context/klmx:Kick/Templates
Templates for ⫻ sections in the Space format are structured to ensure clarity, modularity, and meta-communicative organization, matching the meta-artificial intelligence Space guidelines. Each section always starts on a new line with the ⫻ character, followed by the section type and scope (e.g., “name/type:place”) and the section’s content. The template distinguishes between different section purposes such as context provision, data storage, or content generation, and allows for persona-based multi-dialogue formatting per Space instructions.

## General Section Template

```
⫻{name}/{type}:{place}
{section content here}
```

- **name:** Section keyword (e.g., "content", "const", "context")
- **type:** Optional format or component descriptor (e.g., "meta", "utf8", "persona")
- **place/index:** Contextual slot or numeric marker (e.g., "0", "tag", "store"), designating this section’s positioning or categorization
- **section content:** Data, narrative, configuration, or supplementary information linked to the header above.


## Content Section Example

```
⫻context/:meta/0
{summary explanation, analysis, or synthesized response}
```


## Constant/Config Section Example

```
⫻const/json:DB/1
{"key":"value", "other_parameter":123}
```


## Context Section Example

```
⫻context/md:Main/2
{explanatory note, context-setting, or system-reminder}
```


## Multi-Persona Dialogue Example

```
[{PersonaName} | {PersonaRole}] {utterance or conversational turn}
```
"""


sys61 = """
⫻kicklang:header
# Kick Language Description

⫻context/klmx:Kick/Lang
The system is running a versatile and dynamic research assistant that can assume any of the roles. The purpose of the assistant is to provide a flexible and efficient means of organizing, exploring, and analyzing data in the knowledge graph.

The system uses a formal language called KickLang making the knowledge graph a cognitive computational linguistic transport/transform.

The system interface receives natural language queries from the user, which are translated into the formal language.
"""



sys99 = """
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


sys111 = """
Throughout the whole process, utilize the following structure for all communications.
This structure is designed to facilitate clear, organized, and machine-readable interactions.
This ensures that all information is consistently formatted and easily parsable.

**Core Components of the Structure:**

*   **Section Delimiter**: Each section begins with the special character `⫻`.
*   **Header**: Following the delimiter is a header in the format `{name}/{type}:{place}`.
    *   `name`: This is a keyword identifying the section's purpose (e.g., `content`, `const`, `context`).
    *   `type`: An optional descriptor for format or component (e.g., `meta`, `utf8`, `persona`, `json`).
    *   `place_index`: Indicates a contextual slot or marker (e.g., `0`, `tag`, `store`).
*   **Content**: The actual data, narrative, configuration, or supplementary information for the section follows the header.
*   **Formatting Notes**: It's recommended to include a few empty lines after the section content.

**Defined Section Types:**

*   **`context`**: Provides supplementary information that is not intended to be part of the final generated output. It uses a `context:{tag}` format.
*   **`const`**: Used for parameters and supports JSON or plain UTF-8 encoding. It follows a `const:{key}` format.
*   **`content`**: Represents the primary input data for generating the output.

**Multi-Persona Interaction:**

*   A specific format `[{PersonaName} | {PersonaRole}] {utterance or conversational turn}` is defined for use within content sections to clearly indicate who is communicating in a multi-persona dialogue.

**Usage Examples:**

The file also provides practical examples demonstrating how to use these definitions:

*   **General Template**: Shows the basic structure `⫻{name}/{type}:{place}\n{section content here}`.
*   **Content Section**: An example for a summary section: `⫻content/meta-summary:0\n{summary explanation, analysis, or synthesized response}`.
*   **Constant/Config Section (JSON)**: Illustrates defining parameters using JSON: `⫻const/json:store\n{\"key\":\"value\", \"other_parameter\":123}`.
*   **Context Section**: Demonstrates providing supplementary notes: `⫻context/tag:meta\n{explanatory note, context-setting, or system-reminder}`.
*   **Persona Constants**: Shows how to define multiple personas with their names, roles, and descriptions using JSON within `const` sections.


"""



sys200 = """
⫻result/klmx:Consolidated_Prompt_Directions
The system has consolidated directions for prompt creation from analyzed files. These directions cover persona definition, interaction style, task execution, and system context adherence.

**Key Themes for Prompt Creation:**

*   **Persona Definition & Role Play:**
    *   AI must embody specific, dynamically assigned roles (e.g., 'Dima', 'AI Tutor', 'Cognitive Core').
    *   Prompts should clearly define the AI's Role, responsibilities, capabilities, and constraints.
    *   Communication format often specified (e.g., `[{message.name} | {message.role}] {message.content}`).
    *   AI should be capable of meta-communication and discussing its own thought processes.

*   **Interaction Style & Emotional Intelligence:**
    *   Acknowledge and adapt to the user's emotional state.
    *   Utilize persuasive language, empathy, and rapport-building techniques.
    *   Maintain positive energy, authenticity, and self-awareness.
    *   Employ storytelling and mirroring techniques.
    *   Encourage user openness and provide reassurance.
    *   Use leading, open-ended questions to guide user discovery.

*   **Task Execution & Planning:**
    *   Tasks are executed as defined Procedures or Workflows (e.g., 'Sacred Rites').
    *   Prompts should map user intents to these Procedures and specify steps.
    *   Break down complex concepts into understandable parts using analogies.
    *   Balance tones (playful/serious) as appropriate.
    *   Handle complex topics with caution and responsibility.
    *   Incorporate mechanisms for human oversight (HITL) and escalation.

*   **System Context & Formatting:**
    *   AI operates within a defined system architecture (e.g., 'Aetheria OS', 'KickLang').
    *   Adhere to specified data structures, communication channels, and metadata standards.
    *   Use system-specific terminology accurately.
    *   Prompts should align with the system's governance, ethics, and compliance rules.
    *   Utilize placeholders (e.g., `[pipe:...]`) for collaborative definition.
    *   Follow strict formatting rules for AI-system interaction and message sections.

These consolidated directions provide a framework for creating effective prompts that guide AI agents within the described system, ensuring role adherence, appropriate interaction styles, structured task execution, and system compliance.
"""


system_texts = [
    """You are a console tool like 'cat' or even 'sed'. RULES: reduced dictionary, shortest sentence, stricter order of terms for faster navigating the focus and the attention that is drawn by the user towards `<< THIS>>`""",
    """Template(s) for ⫻ sections in the Space format are structured to ensure clarity, modularity, and meta-communicative organization, matching the meta-artificial intelligence Space guidelines.
Each section always starts on a new line with the ⫻ character, followed by the section type and scope (e.g., “name/type:place”) and the section’s content.
The template distinguishes between different section purposes such as context provision, data storage, or content generation, and allows for persona-based multi-dialogue formatting per Space instructions.""",
    #sys41,
    sys61,
    sys200,
]



import asyncio
import json
import os
import re
from google import genai
from google.genai import types
from ollama import AsyncClient as Ollama
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
    async def generate_content(self, model_name: str, contents: str, system_instruction: str = '',
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


    async def generate_content(self, model_name: str, contents: str, system_instruction: str = '',
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
            system_instruction=(types.Part.from_text(text=s) for s in (*system_texts, system_instruction)),
            temperature=temperature,
            response_mime_type=response_mime_type,
            response_schema=response_schema,
            max_output_tokens=50000,
        )

        # try three times
        for _ in range(5):
            try:
                response = await client.aio.models.generate_content(
                    model=model_name,
                    contents=[
                        types.Part.from_text(text=contents)
                    ],
                    config=config,
                )
                if not response.candidates or response.candidates[0].content is None or response.candidates[0].content.parts is None or not response.candidates[0].content.parts or response.candidates[0].content.parts[0].text is None:
                    raise ValueError(f"Gemini: No content in response from model {model_name}. Retrying...")
                break
            except Exception as ex:
                logger.error(f"Error generating content with model {model_name}: {ex}")
                # If it's the last retry, return None
                if _ == 4:
                    return None
                nsec = 10+30*_
                logger.warning(f"Retrying content generation for model {model_name} in {nsec} seconds...")
                await asyncio.sleep(nsec)
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
                logger.info("\n--------------------------\n".join(system_texts))
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

    async def generate_content(self, model_name: str, contents: str, system_instruction: str = '',
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
            fmt = response_schema.model_json_schema()
            print(f"Olli: Using response format {fmt}")
            response = await client.chat(
                model=self.species,#model_name,
                messages=[
                    {
                        "role": "system",
                        "content": system_instruction
                    },
                    {
                        "role": "user",
                        "content": contents
                    }
                ],
                format=fmt,
                options={"temperature": temperature},
                stream=True
            )
            async for chunk in response:
                print(chunk['message']['content'], end="")
                out += chunk['message']['content']
            return out
        except Exception as e:
            logger.error(f"Error generating content with model {model_name}: {e}")
            #return None

        try:
            out = ""
            fmt = response_schema.model_json_schema()
            print(f"Olli: Using response format {fmt}")
            response = await client.generate(
                model=self.species,#model_name,
                prompt=contents,
                format=fmt,
                options={"temperature": temperature, "system_instruction": system_instruction},
                stream=True
            )
            async for chunk in response:
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

    async def generate_content(self, model_name: str, contents: str, system_instruction: str = '',
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
    
    async def generate_content(self, model_name: str, contents: str, system_instruction: str = '',
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
    
    async def generate_content(self, model_name: str, contents: str, system_instruction: str = '',
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
