# Section Format Specification

This document outlines the specification for the structured section format used in communications, particularly for multi-persona AI interactions. This format ensures structured communication and clear delineation of information, vital for organized and effective exchanges.

## I. General Structure

Each section is clearly delineated and structured as follows:

- **Delimiter:** A ⫻ character marks the beginning of a section, appearing on a new line.
- **Header:** Immediately following the delimiter is the header, which follows the pattern `{name}/{type}:{place/index}`. The colon separates the section identifier (`name/type`) from its positional or categorical marker (`place/index`).
  - **`name`**: The primary keyword or token identifying the section's purpose (e.g., "const", "content", "context").
  - **`type`**: An optional descriptor providing further information about the format, encoding, or component type (e.g., "meta", "utf8", "persona", "json").
  - **`place/index`**: A contextual slot or numeric marker (e.g., "0", "tag", "store", "meta") designating this section's positioning or categorization.
- **Section Content:** The data, narrative, configuration, or supplementary information relevant to the header.

Ensure a few empty lines are present after the section content until the end of the section.

## II. Specific Section Types and Their Purposes

### Context Sections

- **Format:** `⫻context/{tag}:{place}`
- **Purpose:** Provide supplementary information that is relevant to the ongoing interaction but should not be directly included in the generated output. This is useful for system reminders, background information, or meta-notes.
- **Example:** 
```markdown
    ⫻context/tag:meta
    {explanatory note, context-setting, or system-reminder}
```

### Constant/Configuration Sections

- **Format:** `⫻const/{type}:{place}`
- **Purpose:** Serve as parameters or configuration settings. These sections can use JSON format or plain UTF-8 encoding.
- **Note:** While `const` supports plain UTF-8, JSON is a common and recommended encoding for structured parameters within this section type.
- **Examples:** 
```markdown
    ⫻const/json:store
    {"key":"value", "other_parameter":123}
```

```markdown
    ⫻const/utf8:greeting
    Hello there!
```

### Content Sections

- **Format:** `⫻content/{type}:{place}`
- **Purpose:** Provide the primary input data for generating the output. This section can also contain multi-persona dialogues formatted as described in the next section.
- **Example:** 
```markdown
    ⫻content/meta-summary:0
    {summary explanation, analysis, or synthesized response}
```

## III. Multi-Persona Interaction Format

Within a "content" section, individual conversational turns or utterances are formatted to clearly identify the speaker and their role:

- **Format:** `[{PersonaName} | {PersonaRole}] {utterance or conversational turn}`

This format allows for the clear identification of different personas and their contributions to the conversation, aligning with meta-communicative structures.

## IV. Architectural Implications

This structured section format is designed to enhance clarity, modularity, and organization in complex conversational systems. By explicitly defining sections for context, constants, and content, it facilitates:

- **Modularity:** Each section can be managed and processed independently.
- **Clarity:** The clear delineation of information types reduces ambiguity.
- **Scalability:** The format supports complex interactions involving multiple personas and diverse data types.
- **Maintainability:** Structured data is easier to parse, debug, and update.

These templates provide modular layout cues for both AI and human participants in meta-structured interactions.