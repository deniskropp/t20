# Refined Prompt Engineering Guidelines for YouTube Short Script Generation (Co-evolutionary Greetings)

These guidelines have been updated based on feedback to ensure the generated YouTube Short script is highly optimized for clarity, conciseness, pacing, and visual integration, specifically for the Shorts format.

## Core Principles (Emphasized for Shorts):

1.  **Ultra-Conciseness:** Every syllable and visual must serve a purpose. Eliminate any non-essential words or pauses. Aim for ~130-150 words maximum.
2.  **Visual-First Narrative:** Write *for the screen*. Assume visuals carry significant weight. Dialogue should complement, explain, or punctuate the visuals.
3.  **Immediate Hook:** The first 3 seconds are paramount. The hook must be visually arresting and pose an immediate, intriguing question or statement.
4.  **Relentless Pacing:** Maintain an energetic, fast-paced rhythm throughout. Use short sentences, quick cuts in visuals, and dynamic voiceover delivery.
5.  **Simplified Explanations:** Complex concepts must be distilled into the simplest possible terms, using analogies where effective.
6.  **Platform Native:** Adhere strictly to YouTube Shorts constraints (< 60s, vertical 9:16, mobile-first viewing).

## Refined Prompt Structure for Script Generation:

When prompting the script generation agent, include the following elements:

*   **Role:** "You are an expert scriptwriter for high-impact, ultra-short-form video content, specializing in making science engaging for a broad audience on platforms like YouTube Shorts."
*   **Goal:** "Generate a script for a YouTube Short (under 60 seconds, vertical 9:16) that compellingly explains 'co-evolutionary greetings' using vivid examples and dynamic pacing."
*   **Input Data:** Provide the `youtube_short_script_outline_refined.json` file, emphasizing:
    *   The `title`, `logline`, and `target_audience`.
    *   The strict `constraints` (duration, platform, aspect ratio, **hook time (0-3s)**, **pacing (Very fast, dynamic, engaging)**).
    *   The detailed `narrative_arc` breakdown, paying close attention to the `time_estimate_seconds`, `visual_suggestions`, and `dialogue_suggestion` for each segment.
    *   The `core_concepts_to_emphasize` and `key_information_points_for_script` that MUST be integrated.
*   **Specific Instructions for Refinement:**
    *   "Write dialogue that is conversational, punchy, and extremely concise. Aim for a natural, enthusiastic delivery."
    *   "Ensure visual suggestions are dynamic, easily understandable, and directly support the dialogue. Specify actions or camera shots where helpful (e.g., 'Extreme close-up', 'Split screen')."
    *   "The hook (first 0-3 seconds) MUST be visually arresting and immediately pose an intriguing question or statement."
    *   "Maintain a **very fast and dynamic pace** throughout. Use short sentences and quick transitions between ideas and visuals."
    *   "Simplify scientific terms like 'co-evolution' and 'reciprocal adaptation' using clear language or analogies."
    *   "The final script should be approximately 130-150 words."
    *   "Format the output with clear `VISUAL` and `AUDIO (VOICEOVER)` sections for each time segment."
    *   "The concluding question must be direct and clearly prompt audience interaction in the comments."
*   **Tone:** "Highly energetic, curious, awe-inspiring, and extremely concise."

## Example Snippet for Agent Instruction:

```
Generate a YouTube Short script based on the provided refined outline. Prioritize an ultra-fast pace (0-3s hook, <60s total) and extremely concise, engaging dialogue (~140 words). Visuals should be dynamic and directly complement the audio. Ensure the core concepts of co-evolutionary greetings are clearly and simply conveyed.
```

## Iteration Notes:

*   Focus on trimming any redundancy in dialogue or visual descriptions.
*   Ensure the transitions between segments are seamless and contribute to the fast pacing.
*   Verify that the language used is accessible to a general audience with no prior knowledge of the topic.
*   Confirm that the final script aligns perfectly with the refined narrative arc timings and content points.
