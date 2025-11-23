"""
This module defines the CogitoPromptRefinementAgent, a specialized agent for
refining prompts for other agents in the multi-agent system.
"""

import logging
from typing import Optional

from runtime.agent import Agent
from runtime.custom_types import AgentOutput, Task, File
from runtime.core import ExecutionContext

logger = logging.getLogger(__name__)


import json

class CogitoPromptRefinementAgent(Agent):
    """
    An agent that refines prompts for other agents based on feedback and context.
    """

    def execute_task(self, context: ExecutionContext, task: Task) -> Optional[str]:
        """
        Executes the prompt refinement task.

        This method retrieves the original prompt and any associated feedback from the
        execution context, uses an LLM to generate a refined prompt, and then
        returns the new prompt as an artifact.
        """
        logger.info(f"CogitoPromptRefinementAgent is executing task: {task.description}")

        # Find the original prompt and feedback from the context artifacts
        original_prompt = ""
        feedback_list = []

        for item in context.items.values():
            if item.step.id in task.requires:
                if item.name.endswith("_prompt.txt"):
                    original_prompt = item.content
                if item.name.startswith("feedback/"):
                    feedback_list.append(item.content)

        if not original_prompt:
            return "Error: Original prompt not found in context."

        if not feedback_list:
            return "Error: Feedback not found in context."

        # For simplicity, we'll just use the first feedback found
        feedback = json.loads(feedback_list[0])

        refinement_prompt = f"""
You are an expert in prompt engineering. Your task is to refine a prompt for an AI agent based on the provided feedback.

**Original Prompt:**
---
{original_prompt}
---

**Feedback:**
---
{feedback['comment']}
(Rating: {feedback['rating']})
---

Please provide a new, refined prompt that addresses the feedback. The refined prompt should be clear, concise, and effective for the agent's task.
Your output should be only the refined prompt text, without any additional explanation or formatting.
"""

        refined_prompt_text = self.llm.generate_content(
            model_name=self.model,
            contents=refinement_prompt,
            system_instruction=self.system_instructions,
            temperature=0.5,
        )

        if not refined_prompt_text:
            logger.error("LLM failed to generate a refined prompt.")
            return "Error: LLM failed to generate a refined prompt."

        # Create an AgentOutput with the refined prompt as an artifact
        output = AgentOutput(
            output=f"Successfully refined prompt for task '{task.description}'.",
            artifact={
                "files": [
                    File(
                        path=f"refined_prompts/{task.id}_refined_prompt.txt",
                        content=refined_prompt_text.strip()
                    )
                ]
            }
        )

        return output.model_dump_json(indent=4)
