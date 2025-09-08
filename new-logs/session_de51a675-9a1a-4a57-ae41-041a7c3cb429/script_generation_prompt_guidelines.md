# Prompt Engineering Guidelines for YouTube Short Script Generation (Co-evolutionary Greetings)

These guidelines are designed to assist the script generation agent (Qwen3-WebDev) in creating a compelling and effective YouTube Short script based on the provided outline.

## Core Principles:

1.  **Conciseness is Key:** Every word counts. Prioritize brevity and impact. Avoid jargon where possible, or explain it immediately in simple terms.
2.  **Visual Storytelling:** Remember this is for a visual medium. Write with the visuals in mind. Suggest dynamic shots, clear actions, and engaging imagery.
3.  **Hook Emphasis:** The first 5 seconds are critical. Ensure the opening is attention-grabbing and clearly introduces the topic or poses an intriguing question.
4.  **Pacing:** Maintain a fast, energetic pace throughout. Use short sentences and quick transitions.
5.  **Clarity:** Explain complex concepts (like co-evolution) using simple language and relatable analogies.
6.  **Format Adherence:** Strictly adhere to the YouTube Shorts format (< 60 seconds, vertical aspect ratio).

## Prompt Structure for Script Generation:

When prompting the script generation agent, include the following elements:

*   **Role:** "You are a scriptwriter specializing in creating engaging, short-form educational content for YouTube."
*   **Goal:** "Generate a script for a YouTube Short (under 60 seconds) explaining the concept of co-evolutionary greetings."
*   **Input Data:** Provide the `youtube_short_script_outline.json` file, highlighting:
    *   The `title`, `logline`, and `target_audience`.
    *   The specific `constraints` (duration, platform, aspect ratio, hook time, pacing).
    *   The detailed `narrative_arc` breakdown (segment, time estimate, content points, visual suggestions).
    *   The `core_concepts` and `key_information_points` that MUST be included.
*   **Specific Instructions:**
    *   "Develop dialogue that is conversational, clear, and suitable for a general audience."
    *   "Integrate the `visual_suggestions` directly into the script, indicating where they should occur."
    *   "Ensure the hook (first 5 seconds) is highly engaging and clearly sets up the topic."
    *   "Maintain a consistent, fast-paced rhythm throughout the script."
    *   "Incorporate a clear call to action or thought-provoking question at the end."
    *   "Format the output as a script with distinct sections for VISUALS and AUDIO/VOICEOVER."
    *   "Keep the total spoken word count appropriate for a < 60-second video (approx. 120-150 words).
*   **Tone:** "Enthusiastic, curious, and informative."

## Example Snippet for Agent Instruction:

```
Generate a script for a YouTube Short based on the provided outline. Focus on a fast pace and clear explanations. The script should be under 150 words and include distinct visual and audio cues. Ensure the first 5 seconds grab attention and introduce the concept of 'co-evolutionary greetings'.
```

## Iteration Notes:

*   Be prepared to refine the script based on feedback regarding clarity, pacing, and engagement.
*   Ensure scientific accuracy while maintaining simplicity.
*   Prioritize visual descriptions that are easy to imagine or animate.
