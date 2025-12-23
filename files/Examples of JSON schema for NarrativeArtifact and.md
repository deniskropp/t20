<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# Examples of JSON schema for NarrativeArtifact and ContextArtifact

Here are minimal, KickLang-aligned JSON Schema examples you can adapt for your artifacts. These assume your graph-level types (characters, events, etc.) but stay implementation-agnostic.[^1][^2][^5][^6]

## NarrativeArtifact schema

```json
{
  "$id": "https://example.com/schema/NarrativeArtifact.schema.json",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "NarrativeArtifact",
  "type": "object",
  "properties": {
    "planId": {
      "type": "string",
      "description": "Globally unique identifier of the PLAN episode that produced this artifact."
    },
    "depth": {
      "type": "integer",
      "minimum": 0,
      "description": "Nesting depth of the producing PLAN in the cognitive stack."
    },
    "prose": {
      "type": "string",
      "description": "Human-readable narrative output (e.g., story segment)."
    },
    "tone": {
      "type": "string",
      "description": "Narrative tone parameter (e.g., Epic, Dark, Neutral)."
    },
    "worldStateSnapshot": {
      "type": "object",
      "description": "Optional summarized state of key world entities at the end of this segment.",
      "additionalProperties": true
    },
    "graphDiffs": {
      "type": "array",
      "description": "Knowledge-graph updates implied by this narrative.",
      "items": {
        "type": "object",
        "properties": {
          "subject": { "type": "string" },
          "predicate": { "type": "string" },
          "object": { "type": "string" },
          "op": {
            "type": "string",
            "enum": ["add", "remove", "update"]
          }
        },
        "required": ["subject", "predicate", "object", "op"],
        "additionalProperties": false
      }
    },
    "metadata": {
      "type": "object",
      "description": "Free-form meta, e.g., length, safety flags, model info.",
      "additionalProperties": true
    }
  },
  "required": ["planId", "prose"],
  "additionalProperties": false
}
```


## ContextArtifact schema

```json
{
  "$id": "https://example.com/schema/ContextArtifact.schema.json",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "ContextArtifact",
  "type": "object",
  "properties": {
    "contextId": {
      "type": "string",
      "description": "Identifier for this context snapshot."
    },
    "originPlanId": {
      "type": "string",
      "description": "PLAN that assembled this context (if applicable)."
    },
    "storyRequest": {
      "type": "string",
      "description": "User prompt or continuation request piped into the pipeline."
    },
    "timeHorizon": {
      "type": "string",
      "enum": ["ShortTerm", "MediumTerm", "LongTerm"],
      "description": "Planning horizon parameter used by Planner roles."
    },
    "entities": {
      "type": "array",
      "description": "Relevant graph entities (characters, locations, events, items, concepts).",
      "items": {
        "type": "object",
        "properties": {
          "id": { "type": "string" },
          "kind": {
            "type": "string",
            "enum": ["Character", "Location", "Event", "Item", "Concept"]
          },
          "labels": {
            "type": "array",
            "items": { "type": "string" }
          },
          "traits": {
            "type": "object",
            "description": "Key–value traits such as hastrait, state flags, etc.",
            "additionalProperties": true
          }
        },
        "required": ["id", "kind"],
        "additionalProperties": false
      }
    },
    "relations": {
      "type": "array",
      "description": "Pre-extracted edges from the knowledge graph.",
      "items": {
        "type": "object",
        "properties": {
          "subject": { "type": "string" },
          "predicate": {
            "type": "string",
            "enum": [
              "hastrait",
              "locatedin",
              "precedes",
              "interactswith",
              "possesses"
            ]
          },
          "object": { "type": "string" }
        },
        "required": ["subject", "predicate", "object"],
        "additionalProperties": false
      }
    },
    "pipes": {
      "type": "object",
      "description": "Placebo pipes visible at this boundary (storyrequest, worldstate, etc.).",
      "properties": {
        "storyrequest": { "type": "string" },
        "worldstate": { "type": "object" },
        "characterupdate": { "type": "object" },
        "plotpoint": { "type": "string" },
        "synthesisoutput": { "type": "string" }
      },
      "additionalProperties": true
    },
    "contextSignature": {
      "type": "object",
      "description": "Schema-like summary of what this context guarantees to contain.",
      "additionalProperties": true
    }
  },
  "required": ["contextId"],
  "additionalProperties": false
}
```


## How they fit KickLang

- ContextArtifact matches the CLUSTER/FIND output over Characters, Locations, Events, Items, Concepts plus key edges, and optionally carries current placebo pipes.[^3][^1]
- NarrativeArtifact matches SUMMARIZE + TRANSFORM outputs plus graph LINK operations encoded as `graphDiffs`, and can be traced back to the producing PLAN via `planId` and `depth`.[^2][^1]

If you share your current pipeline contract (fields you already log), these schemas can be tightened with stricter enums and required sets.
<span style="display:none">[^10][^11][^12][^13][^14][^4][^7][^8][^9]</span>

<div align="center">⁂</div>

[^1]: kicklang-synthesis-objective-m-R_dnjarHQxOY8hblQMCb0A.md

[^2]: this-is-solid-and-more-than-th-3FjwxRxoTDifMknLoT89qw.md

[^3]: Absolutely-lets-take-that-outline-and-turn-it-i.pdf

[^4]: One-liner-about-KickLang.md

[^5]: https://json-schema.github.io/json-schema/example1.html

[^6]: https://json-schema.org/learn/json-schema-examples

[^7]: https://json-schema.org/learn/miscellaneous-examples

[^8]: https://docs.pydantic.dev/latest/api/json_schema/

[^9]: https://github.com/jfrog/build-info/issues/82

[^10]: https://json-schema.org/understanding-json-schema/structuring

[^11]: https://www.ietf.org/archive/id/draft-bhutton-json-schema-01.html

[^12]: https://stackoverflow.com/questions/7341537/tool-to-generate-json-schema-from-json-data

[^13]: https://json-schema.org/specification

[^14]: https://github.com/dragonwasrobot/json_schema

