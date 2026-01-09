# Chapter 4: Action Verbs (Knowledge Access)

KickLang uses a specific set of **Action Verbs** to interact with information. These verbs are the primary way agents "see" and "retrieve" data.

## The Big Three: FIND, LIST, DETAIL

### 1. FIND
Use `FIND` to search for specific entities or concepts based on a query or filter.

**Syntax:**
```kicklang
FIND TargetEntity [FilterParameters] [Limit] → [OutputVariable]
```

**Examples:**
```kicklang
# Find a specific entity by ID/Name
FIND EntityContext context

# Find with a filter
FIND EntityScene FilterHasTrait=TensionHigh → <<scary_scenes>>

# Find with a text query
FIND EntityConcept "The meaning of life" Limit3 → <<results>>
```

### 2. LIST
Use `LIST` to enumerate items without retrieving their full content. This is useful for browsing or getting an overview.

**Syntax:**
```kicklang
LIST TargetCollection [FilterParameters] → [OutputVariable]
```

**Example:**
```kicklang
LIST AllCharacters FilterLocation=Library → <<characters_in_library>>
```

### 3. DETAIL
Use `DETAIL` to get the full, high-resolution content of a specific entity or list of entities found previously.

**Syntax:**
```kicklang
DETAIL TargetEntity → [OutputVariable]
```

**Example:**
```kicklang
# First list them
LIST AllArtifacts → <<artifacts>>
# Then get details for the first one (or all, depending on implementation)
DETAIL <<artifacts>> → <<full_description>>
```

## Tips for Access
- **Granularity Matters**: If you just need to know *if* something exists, use `LIST` or `FIND` with a limit. Only use `DETAIL` when you need the full text/attributes, as it consumes more context.
- **Variables**: Store results in `<<placebo_pipes>>` (variables) to pass them to transformation verbs later.

In the next chapter, we will discuss how to **transform** and **structure** this data using verbs like `SUMMARIZE`, `LINK`, and `CLUSTER`.
