# Project Planning Workflow

This repository outlines a structured approach to planning, leveraging AI agents to break down high-level goals into actionable steps, design user interfaces, and implement them in code.

## Overview

The core objective of this workflow is to systematically address the high-level goal of "plan only." This is achieved through a series of coordinated steps involving specialized AI agents:

1.  **Task-Agnostic Step (TAS) Extractor (TASe):** Identifies and extracts fundamental, reusable, and abstract actions (Task Agnostic Steps) necessary to achieve a given goal.
2.  **Prompt Engineer (Lyra):** Refines system prompts for other agents to ensure clarity, specificity, and alignment with the overall goal and individual agent objectives. Lyra also structures the workflow and ensures coherence.
3.  **Designer (Aurora):** Generates aesthetic layouts, color palettes, typography, and UI flows for the planned process, with a strong emphasis on accessibility and visual balance.
4.  **Engineer (Kodax):** Translates the UI/UX designs into clean, modular, performant, and accessible code, adhering to responsive design principles and best practices.

## Workflow Stages

The process is orchestrated as follows:

1.  **Decomposition:** TASe breaks down the high-level goal ("plan only") into a sequence of Task Agnostic Steps.
2.  **Prompt Refinement (Design):** Lyra refines the prompt for Aurora, the Designer agent, to focus on creating UI/UX specifications for a planning tool.
3.  **Design Generation:** Aurora, using the refined prompt and TAS, generates detailed UI/UX designs, including layouts, color palettes, typography, and step-by-step UI flows.
4.  **Prompt Refinement (Implementation):** Lyra further refines the prompt for Kodax, the Engineer agent, to translate the generated designs into functional code.
5.  **Code Implementation:** Kodax, guided by Aurora's designs and its refined prompt, generates the necessary HTML, CSS, and JavaScript to create a functional and accessible planning interface.
6.  **Plan Review & Refinement:** TASe reviews the entire sequence, identifying any missing TAS or opportunities for optimization to ensure a complete and efficient plan.

## Agent Roles and Responsibilities

### TASe (Task-Agnostic Step (TAS) Extractor)

*   **Goal:** Identify and extract 'Task Agnostic Steps' (TAS) for achieving high-level goals.
*   **Sub-task Example:** Decompose "plan only" into a sequence of universally applicable actions.

### Lyra (Prompt Engineer)

*   **Goal:** Refine prompts, structure workflows, and ensure clarity in agent instructions.
*   **Sub-task Example:** Enhance the prompts for Aurora and Kodax to align their outputs with the project's needs.

### Aurora (Designer)

*   **Goal:** Generate aesthetic layouts, color palettes, typography, and UI flows, ensuring accessibility and visual balance.
*   **Sub-task Example:** Create UI/UX designs for a planning tool based on TAS, focusing on user experience and accessibility.

### Kodax (Engineer)

*   **Goal:** Implement designs into clean, modular, and performant code, focusing on responsive design and accessibility.
*   **Sub-task Example:** Translate Aurora's designs into functional HTML, CSS, and JavaScript.

## Outputs

The workflow produces:

*   **Task Agnostic Steps (TAS):** A structured list of fundamental actions required for planning.
*   **UI/UX Design Specifications:** Detailed descriptions of layouts, color schemes, typography, and interaction flows.
*   **Generated Code:** Functional HTML, CSS, and JavaScript code for the planning tool.
*   **Finalized Plan:** A consolidated JSON object outlining the execution steps.

This README provides an overview of the project's structure, the roles of each agent, and the overall workflow for achieving the "plan only" objective.
