# Introduction

## Purpose and Scope of the Runtime Documentation

This document provides comprehensive guidance on the runtime system, detailing its architecture, core components, usage, and advanced features. The scope covers the entire lifecycle of the runtime, from initial setup to advanced customization.

## Target Audience

This documentation is intended for software developers, system administrators, and researchers who need to understand, integrate with, or extend the runtime system. A foundational understanding of Python and software development concepts is beneficial.

## Overview of Runtime Components

The runtime system is composed of several key components:

*   **Agents:** Individual units of work, each with a specific role and goal, powered by LLMs.
*   **Sessions:** Manages the state and artifacts of a particular workflow execution.
*   **ExecutionContext:** Holds the context for a specific step or round within a workflow.
*   **Orchestrator:** Responsible for planning and managing the overall workflow.
*   **System:** The main class that orchestrates the setup and execution of the entire system.
*   **LLM Abstraction:** A layer that allows for integration with various Large Language Models.
