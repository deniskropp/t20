# Chapter 5: Action Verbs (Transform & Structure)

Once you have accessed data using `FIND` or `LIST`, you usually need to process it. KickLang provides powerful verbs for structuring and transforming knowledge.

## Knowledge Structuring

### 1. LINK
Connects two nodes in the knowledge graph.

**Syntax:**
```kicklang
LINK SourceNode, EdgeType, TargetNode; [EdgeAttributes]
```

**Examples:**
```kicklang
LINK CharacterAlice, interacts_with, CharacterBob; Tone=Hostile
LINK Scene1, precedes, Scene2
```

### 2. CLUSTER
Groups entities based on shared attributes or semantic similarity.

**Syntax:**
```kicklang
CLUSTER InputCollection [Criteria] → [OutputCluster]
```

**Example:**
```kicklang
CLUSTER <<search_results>> ByTopic → <<topic_clusters>>
```

### 3. MAP
Traverses the graph to reveal relationships.

**Syntax:**
```kicklang
MAP NodeStart - [Relationship] - NodeEnd [ViewMode]
```

**Example:**
```kicklang
# Show the timeline starting from Scene1
MAP Scene1 - precedes - * → <<timeline>>
```

## Knowledge Transformation

### 1. SUMMARIZE
Condenses information into a shorter form.

**Syntax:**
```kicklang
SUMMARIZE InputData [StyleParameter] → [Output]
```

**Example:**
```kicklang
SUMMARIZE <<long_report>> ToneExecutive → <<exec_summary>>
```

### 2. COMPARE
Analyzes differences or similarities between entities.

**Syntax:**
```kicklang
COMPARE EntityA EntityB [Criteria] → [Output]
```

**Example:**
```kicklang
COMPARE CharacterHero CharacterVillain Traits → <<conflict_analysis>>
```

### 3. EXPLAIN
Generates an explanation or definition for a concept.

**Syntax:**
```kicklang
EXPLAIN Concept [TargetAudience] → [Output]
```

**Example:**
```kicklang
EXPLAIN QuantumPhysics AudienceFiveYearOld → <<simple_explanation>>
```

In the next chapter, we will explain the syntax `<<variable_name>>` we've been using, known as **Placebo Pipes**.
