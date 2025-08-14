```json
{
  "steps": [
    {
      "role": "Task-Agnostic Step (TAS) extractor",
      "task": "Identify and extract the Task Agnostic Steps (TAS) required to achieve the high-level goal of 'refactoring'. This includes identifying areas for improvement, setting refactoring goals, and defining success metrics."
    },
    {
      "role": "Prompt Engineer",
      "task": "Refine the prompts for the Designer and Engineer agents to ensure clarity and focus on the refactoring goals. This includes specifying the desired aesthetic improvements and code quality standards."
    },
    {
      "role": "Designer",
      "task": "Generate aesthetic layouts, color palettes, typography, and UI flows for the refactored components, ensuring accessibility and visual balance. Focus on improving the user experience and visual appeal of the identified areas."
    },
    {
      "role": "Engineer",
      "task": "Implement the designs into clean, modular, and performant code, focusing on responsive design and accessibility. Refactor the existing code based on the design specifications and identified areas for improvement."
    },
    {
      "role": "Prompt Engineer",
      "task": "Review the code and design implementations, providing feedback to the Engineer and Designer agents to ensure alignment with the refactoring goals and quality standards. Refine prompts as needed based on the feedback."
    },
    {
      "role": "Task-Agnostic Step (TAS) extractor",
      "task": "Evaluate the refactoring results against the defined success metrics. Identify any remaining areas for improvement and iterate on the design and implementation as needed."
    }
  ]
}
```
