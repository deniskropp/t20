# KickLang Grammar

## Sample KickLang Grammar (EBNF)

### 1. Overview

This EBNF captures both the **Role‐Preset Definitions** and the **Dialogue/Interaction** sections of a KickLang file. It’s designed for clarity and extensibility, so you can layer in custom fields like `version` or `placeholders` as needed.

### 2. Grammar Rules

```ebnf
KickLangFile       ::= RoleDefinitions , DialogueSection? ;

RoleDefinitions    ::= { RoleDefinition } ;

RoleDefinition     ::= "role" , Identifier , "{" , RoleField* , "}" ;

RoleField          ::= Identifier , ":" , ( StringLiteral | ListLiteral ) ;

ListLiteral        ::= "[" , ListElement , { "," , ListElement } , "]" ;

ListElement        ::= StringLiteral | Identifier ;

DialogueSection    ::= DialogueLine+ ;

DialogueLine       ::= "[" , Identifier , "|" , Identifier , "]" , MessageContent ;

MessageContent     ::= { CharacterExceptNewline } , "\n" ;

Identifier         ::= Letter , { Letter | Digit | "_" } ;

StringLiteral      ::= "\"" , { CharacterExceptQuote } , "\"" ;

Letter             ::= "A"… "Z" | "a"… "z" ;

Digit              ::= "0"… "9" ;

CharacterExceptNewline ::= ? any char except newline ? ;

CharacterExceptQuote   ::= ? any char except double-quote ? ;
```

### 3. Explanation of Key Productions

- `RoleDefinition`   Declares a named preset. Fields inside can be persona, objectives, acts, style, version, etc.
- `RoleField`   Maps a key (like `acts`) to either a string (`"Reflective"`) or a list (`[REQUEST, INFORM]`).
- `DialogueLine`   Binds an agent instance (`AgentName`) to a role (`RoleName`) and captures free‐form message text.
- `Identifier` & `StringLiteral`   Basic lexical tokens; identifiers for names, quoted strings for descriptive values.

### 4. Next Steps & Related Ideas

- build an ANTLR4 grammar to generate a parser/AST in Java, Python, or JavaScript
- implement a CLI linter that checks missing fields, mismatched role names, or deprecated acts
- create unit tests with sample `.kl` files covering inheritance, dynamic role swapping, and custom placeholders
- integrate a JSON schema export so tools like VS Code can offer autocomplete and inline validation

Would you like a full ANTLR4 grammar definition or a starter parser script in your language of choice? Let me know and we can dive deeper into implementation details.







## Full ANTLR4 Grammar Definition for KickLang

Below is a complete ANTLR4 grammar (`KickLang.g4`) capturing both **Role‐Preset Definitions** (with optional inheritance and custom fields) and the **Dialogue/Interaction** sections. You can plug this into ANTLR4 directly to generate a parser/lexer in Java, Python, JavaScript, etc.

```antlr
grammar KickLang;

// Parser Rules

kickLangFile
    : roleDefinitions dialogueSection? EOF
    ;

roleDefinitions
    : roleDefinition*
    ;

roleDefinition
    : 'role' IDENT ( 'extends' IDENT )? '{' roleField* '}'
    ;

roleField
    : IDENT ':' value
    ;

value
    : STRING
    | listLiteral
    ;

listLiteral
    : '[' listElement (',' listElement)* ']'
    ;

listElement
    : STRING
    | IDENT
    ;

dialogueSection
    : dialogueLine+
    ;

dialogueLine
    : '[' IDENT '|' IDENT ']' MESSAGE_CONTENT
    ;

// Lexer Rules

// Matches agent or role names, field keys
IDENT
    : [A-Za-z_] [A-Za-z_0-9]*
    ;

// Quoted strings for persona, style, etc.
STRING
    : '"' ( '\\' . | ~["\\] )* '"'
    ;

// Captures everything on a dialogue line after the prefix
MESSAGE_CONTENT
    : (~[\r\n])+
    ;

// Whitespace (spaces/tabs), skip but not newlines
WS
    : [ \t]+ -> skip
    ;

// Newlines, skipped to simplify MESSAGE_CONTENT handling
NEWLINE
    : '\r'? '\n' -> skip
    ;

// Single‐line comments
COMMENT
    : '//' ~[\r\n]* -> skip
    ;
```

### Explanation of Key Sections

- kickLangFile Entry point combining all role presets and optional dialogue.
- roleDefinition Supports `role Name { ... }` plus optional `extends BaseRole` for inheritance.
- roleField & value Any custom field (e.g., `persona`, `objectives`, `acts`, `style`, `version`, `placeholders`, `contextFiles`) maps an identifier to either a quoted string or a list.
- dialogueLine Matches `[AgentName|RoleName]` prefixes followed by free‐form text (`MESSAGE_CONTENT`).
- Lexer rules Define identifiers (`IDENT`), strings (`STRING`), and strip comments/whitespace for a clean token stream.

### Integration & Usage

1. Generate Parser/Scanner
   - `antlr4 -Dlanguage=Java KickLang.g4`
   - Or replace `-Dlanguage=Java` with `Python3`, `JavaScript`, etc.
2. Build an AST or Visitor
   - Implement a visitor (`KickLangBaseVisitor`) to walk `kickLangFile` and build in‐memory models for roles and dialogues.
3. Add Semantic Actions
   - Enforce required fields (`persona`, `acts`, etc.).
   - Validate that every `IDENT` in `[AgentName|RoleName]` matches a defined `roleDefinition`.
4. Integrate with Tooling
   - Wire up in a CLI linter for `.kl` files.
   - Export JSON schema for IDE autocomplete (VS Code extension).

## Next Steps & Questions

- Would you like a **starter parser script** in Java or Python that uses this grammar and demonstrates AST construction?
- Interested in **error‐recovery strategies** (e.g., missing braces, unknown acts)?
- Want to explore **custom listeners** to emit KickLang→JSON or KickLang→YAML transforms?