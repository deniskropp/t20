# Chapter 6: Placebo Pipes (Variables)

You've seen the `<<variable_name>>` syntax in previous chapters. In KickLang, these are formally called **Placebo Pipes**.

## Why "Placebo"?
They are called "Placebo Pipes" because they don't *do* anything on their own. They act as containers, placeholders, or markers for data flowing through the system. They "trick" the system into treating intermediate states as tangible objects.

## Syntax
A Placebo Pipe is always enclosed in double angle brackets:

```kicklang
<<variable_name>>
```

## Usage Patterns

### 1. As Variables (Data Flow)
Store the output of one stage and pass it to the next.

```kicklang
Stage1 FIND Data → <<raw_data>>
Stage2 SUMMARIZE <<raw_data>> → <<summary>>
Stage3 OUTPUT <<summary>>
```

### 2. As Input Parameters
Define expected inputs for a module or pattern.

```kicklang
⫻module:StoryGenerator <<genre>> <<protagonist>>
```

### 3. As Meta-Markers
Use them to flag states for the system or user to notice, even if not fully computed yet.

```kicklang
LINK Scene1, produces, <<narrative_gap>>
```

## Scope
- **Local:** By default, a pipe created in a `PLAN` is available to subsequent stages in that `PLAN`.
- **Return Values:** The last pipe in a chain is often the implicit return value of the pipeline, or explicitly returned via `⫻output`.

## Best Practices
- Use `snake_case` for pipe names (e.g., `<<user_query>>`, `<<search_results>>`).
- Be descriptive. `<<x>>` is bad; `<<filtered_candidates>>` is good.

In the next chapter, we will learn how to make decisions using **Conditional Logic**.
