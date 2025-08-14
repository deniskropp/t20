# Task-Agnostic Plan Generator

This project provides a framework for generating task-agnostic plans, breaking down complex goals into a series of fundamental, reusable, and abstract actions. These plans can then be used to guide various agents in executing specific tasks.

## Project Overview

The core idea is to define a set of "Task Agnostic Steps" (TAS) that represent the fundamental stages of any planning or problem-solving process. These TAS are then used by various agents (Designer, Engineer, Prompt Engineer, TAS Extractor) to collaborate on creating comprehensive and adaptable plans.

This README outlines the overall architecture, the roles of different agents, and the process of generating task-agnostic plans.

## Team Roles and Goals

*   **Aurora (Designer):** Generates aesthetic layouts, color palettes, typography, and UI flows, ensuring accessibility and visual balance. Also responsible for creating example prompts that demonstrate how to use the task-agnostic plan to guide task execution.
*   **Kodax (Engineer):** Implements designs into clean, modular, and performant code, focusing on responsive design and accessibility. Responsible for implementing systems that allow users to input goals and generate task-specific plans.
*   **Lyra (Prompt Engineer):** Refines prompts, structures workflows, and ensures clarity in agent instructions. Analyzes agent outputs for clarity and alignment with the overall goal.
*   **TASe (Task-Agnostic Step (TAS) Extractor):** Identifies and extracts "Task Agnostic Steps" (TAS) for achieving high-level goals.

## Workflow for Creating a Task-Agnostic Plan

1.  **Define High-Level Goal:** The process begins with a clear, overarching objective (e.g., "create a task agnostic plan").
2.  **Extract Task-Agnostic Steps (TAS):** The TASe agent, guided by Lyra's refined prompts, identifies and extracts the fundamental steps required to achieve the high-level goal.
3.  **Structure and Refine TAS:** Lyra reviews and refines the extracted TAS for clarity, conciseness, and applicability.
4.  **Develop Visual Representation:** Aurora creates a visual representation of the TAS, often a flowchart, to illustrate the sequence and interdependencies.
5.  **Structure TAS Data:** Kodax translates the TAS into a structured format (like JSON) for easy parsing and utilization.
6.  **Create Example Prompts:** Aurora designs example prompts to demonstrate how to use the TAS for specific tasks and how to adapt them.
7.  **Implement Plan Generation System:** Kodax builds a system that allows users to input a high-level goal and automatically generate a task-specific plan based on the TAS. This includes error handling and validation.
8.  **Design User Interface:** Aurora designs a user-friendly and accessible interface for users to interact with the system, input goals, view plans, and provide feedback.

## System Architecture Overview

The system is designed to be modular, with each agent responsible for specific aspects of the plan generation process. The key modules and their interactions are:

*   **TASe (TAS Extractor):** Identifies raw, task-agnostic steps.
*   **Prompt Engineering (Lyra):** Defines and refines the instructions for other agents.
*   **Design (Aurora):** Creates visual representations and example prompts.
*   **Engineering (Kodax):** Implements the core logic, data structures, and user interfaces.

The collaboration between these agents ensures a robust and adaptable planning framework.

## Example TAS Definitions

The following Task Agnostic Steps have been identified as crucial for creating a task-agnostic plan:

*   **Define Objectives:** Establish clear and measurable goals.
*   **Gather Information:** Collect relevant data and insights.
*   **Analyze Data:** Identify patterns, trends, and derive insights.
*   **Develop Solutions:** Generate a range of potential solutions.
*   **Evaluate Options:** Assess the feasibility and risks of each solution.
*   **Select Solution:** Choose the best solution based on evaluation.
*   **Develop Implementation Plan:** Create a detailed plan for execution.
*   **Execute Plan:** Carry out the tasks outlined in the plan.
*   **Monitor Progress:** Track progress and identify deviations.
*   **Adjust Plan:** Make necessary adjustments based on monitoring.

## Technologies and Design Principles

*   **Modularity:** The system is built with modular components to allow for easy modification and extension.
*   **Accessibility:** Adherence to WCAG guidelines is a key principle, ensuring usability for all users.
*   **Responsiveness:** The user interface is designed to be responsive, adapting to various devices and screen sizes.
*   **Clear Prompting:** Prompts are designed for clarity, conciseness, and specificity to ensure accurate agent execution.
*   **Structured Data:** Task-agnostic steps are represented in structured formats like JSON for easy machine readability and interoperability.

## Getting Started

To understand the detailed outputs and prompts generated by each agent, please refer to the specific step files in the project's session directory.

This README provides a high-level overview of the project's structure, goals, and the collaborative process employed to generate task-agnostic plans.
