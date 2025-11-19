# Message Section Definitions

A schema for structuring messages, defining a standardized format for delineating and organizing various types of information within AI and conversational systems.

## Sections

### Section Structure

Defines the fundamental format for all sections within a message.

**Components:**

*   **Section Delimiter**: A special character that marks the beginning of each section.
    *   Value: `⫻`
*   **Section Header**: Follows the delimiter and specifies the section's identity and context.
    *   Format: `{name}/{type}:{place_index}`
    *   **Fields**:
        *   `name`: A keyword identifying the section's primary purpose (e.g., `content`, `const`, `context`).
        *   `type`: An optional descriptor for the format or component type (e.g., `meta`, `utf8`, `persona`, `json`).
        *   `place_index`: Indicates a contextual slot or marker for placement (e.g., `0`, `tag`, `store`).
*   **Section Content**: The actual data, narrative, configuration, or supplementary information for the section.
*   **Formatting Notes**: Ensures a few empty lines are present after the section content until the end of the section for visual separation and parsing.

### Defined Section Types

Categorizes sections based on their intended use and how their content is processed.

*   **`context`**
    *   Format: `context:{tag}`
    *   Description: Provides supplementary information or background context. Its content is not included in the final generated output.
    *   Notes: Useful for system reminders, explanations, or setting the stage.
*   **`const`**
    *   Format: `const:{key}`
    *   Description: Defines constants, parameters, or configuration settings. Content can be JSON or plain UTF-8 encoded.
    *   Notes: Essential for controlling system behavior or providing necessary data.
*   **`content`**
    *   Description: Holds the primary input data, narrative, or instructions for generating the output.
    *   Notes: Serves as the main substance or payload for the generation process.

### Multi-Persona Interaction Format

A specific format used within `content` sections to denote conversational turns by different participants.

*   Format: `[{PersonaName} | {PersonaRole}] {utterance or conversational turn}`
*   Usage: Clearly indicates who is communicating in a multi-persona dialogue.

## Examples

*   **General Section Template**
    *   Description: Illustrates the basic structure applicable to any section.
    *   Code:
        ```
        ⫻{name}/{type}:{place}
        {section content here}
        ```
*   **Content Section Example**
    *   Description: A typical `content` section used for summaries or synthesized responses.
    *   Code:
        ```
        ⫻content/meta-summary:0
        {summary explanation, analysis, or synthesized response}
        ```
*   **Constant/Config Section Example (JSON)**
    *   Description: Demonstrates using a `const` section to define parameters in JSON format.
    *   Code:
        ```
        ⫻const/json:store
        {"key":"value", "other_parameter":123}
        ```
*   **Context Section Example**
    *   Description: Shows how to provide supplementary information using a `context` section.
    *   Code:
        ```
        ⫻context/tag:meta
        {explanatory note, context-setting, or system-reminder}
        ```
*   **Persona Constants Example**
    *   Description: Illustrates defining multiple personas using `const` sections with JSON content.
    *   Code:
        ```
        ⫻const/json:persona
        {
          "name": "Kick La Metta",
          "role": "Meta-AI Coordinator",
          "description": "Coordinates meta-AI activities and ensures seamless collaboration."
        }
        ⫻const/json:persona
        {
          "name": "Denis",
          "role": "Human User",
          "description": "Interacts with the system, providing natural language queries and feedback."
        }
        ⫻const/json:persona
        {
          "name": "Buzz",
          "role": "AI Entity",
          "description": "Executes structured actions based on KickLang DaRolez commands."
        }
        ⫻const/json:persona
        {
          "name": "Fizz",
          "role": "AI Entity",
          "description": "Executes structured actions based on KickLang DaRolez commands."
        }
        ```