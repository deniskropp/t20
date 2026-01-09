# Chapter 8: The Knowledge Graph

KickLang isn't just processing text strings; it operates on a structured **Knowledge Graph**. This graph persists across pipeline stages (and potentially across sessions), acting as the shared memory for all roles.

## Graph Structure

### Nodes (Entities)
Everything is a Node.
- **Concepts**: `Freedom`, `The Color Red`
- **Objects**: `The Holy Grail`, `UserFile.txt`
- **Events**: `Scene1`, `The Battle of Hoth`
- **Agents/Users**: `User123`, `AgentSmith`

Nodes have:
- **ID**: Unique identifier.
- **Type**: e.g., `Scene`, `Character`, `Concept`.
- **Attributes**: Key-value pairs (e.g., `Tone=Dark`).

### Edges (Relationships)
Nodes are connected by explicit relationships.
- `Scene1 -- precedes --> Scene2`
- `CharacterA -- interacts_with --> CharacterB`
- `ObjectX -- located_in --> RoomY`

## Using the Graph

### Reading
You read the graph using `FIND`, `MAP`, and `COMPARE`.
- `FIND` locates nodes by ID or attribute.
- `MAP` traverses edges to find connected nodes.

```kicklang
# Find all scenes that precede the Climax
MAP SceneClimax - precedes(reverse) - *
```

### Writing
You modify the graph using `LINK` and `CLUSTER`.

```kicklang
# Create a new relationship
LINK Hero, possesses, MagicSword

# Update an attribute (implicitly)
LINK Scene1, has_trait, Tense
```

## Why a Graph?
1. **Context**: Roles don't need to read a 100-page document. They just query the graph for relevant nodes.
2. **Memory**: If a pipeline ends, the graph remains. A subsequent pipeline can pick up where the first left off.
3. **Reasoning**: Agents can traverse relationships to infer new connections (e.g., "If A is near B, and B is near C, is A near C?").

In the next chapter, we will learn how to package your code into reusable **Modules** and **Patterns**.
