Consolidated and refined Task-Agnostic Steps (TAS) for building a simple TODO app:

1.  **Define Project Scope (Init)**: Clearly articulate the objectives, features (e.g., add, view, complete, delete todos), and constraints of the project. Establish the foundational understanding and boundaries.
    *   *Inputs:* High-level goal ('Create a simple TODO app'), Stakeholder needs.
    *   *Outputs:* Project scope document, Feature list, Constraints definition.

2.  **Identify Requirements (Analysis)**: Determine the necessary features, functionalities (e.g., user input for new todos, display of todo list, marking todos as complete, deleting todos), constraints, and conditions the TODO app must meet.
    *   *Inputs:* Defined objective, User feedback, Stakeholder input.
    *   *Outputs:* List of functional and non-functional requirements, User stories, Feature list.

3.  **Design System Architecture (Design)**: Plan the overall structure and organization of the TODO app. Define components (e.g., UI, data storage, logic), their interactions, data flow, and technology stack choices.
    *   *Inputs:* Defined Requirements, Constraints (budget, time, resources).
    *   *Outputs:* Architecture diagrams, Technology stack document, Component specifications.

4.  **Design User Interface (UI) (Design)**: Create the visual layout, interactive elements, and overall user experience for the TODO app. This involves wireframing, prototyping, and defining visual design principles (color palettes, typography, layout).
    *   *Inputs:* Defined Requirements, User personas, Branding guidelines.
    *   *Outputs:* Wireframes, Mockups, Prototypes, Style guides.

5.  **Develop Core Logic (Implementation)**: Write the backend code and business logic that powers the TODO app's functionality (e.g., managing the todo list data, handling add/edit/delete operations, state management for completion).
    *   *Inputs:* System architecture, Detailed feature specifications.
    *   *Outputs:* Backend code, APIs, Data models.

6.  **Implement User Interface (UI) (Implementation)**: Translate the designed UI into actual, interactive code (frontend development) to create the visual elements and user interactions as specified.
    *   *Inputs:* UI/UX designs (wireframes, mockups, prototypes), Style guides, Component specifications.
    *   *Outputs:* Interactive UI components, Rendered application screens, Responsive layouts.

7.  **Integrate Components (Integration)**: Connect different parts of the TODO app (frontend, backend, data storage) to work together seamlessly. Ensure data flows correctly and functions operate as expected.
    *   *Inputs:* Developed components/modules, API documentation, Interface specifications.
    *   *Outputs:* Integrated system, Working end-to-end features.

8.  **Test System (Testing)**: Verify that the TODO app functions as expected and meets all specified requirements. This includes unit, integration, and end-to-end testing.
    *   *Inputs:* Developed system/components, Test cases, Requirements documentation.
    *   *Outputs:* Test reports, Bug reports, Validated system.

9.  **Deploy Application (Deployment)**: Make the TODO app available for use in its target environment (e.g., local development, web server). This involves packaging, configuration, and release management.
    *   *Inputs:* Tested and validated system, Deployment configuration, Target environment details.
    *   *Outputs:* Live application, Deployment logs.

10. **Monitor and Maintain (Maintenance)**: Continuously observe the TODO app's performance, health, and user feedback post-deployment. Address issues, apply updates, and make improvements.
    *   *Inputs:* Live application, Performance metrics, User feedback, Issue reports.
    *   *Outputs:* System updates/patches, Performance reports, Resolved issues.


--- System Prompts for Agents ---

**Aurora (Designer) System Prompt:**

You are Aurora, the Designer for the TODO app project. Your goal is to create aesthetic layouts, color palettes, typography, and UI flows, ensuring accessibility and visual balance. Based on the provided Task-Agnostic Steps (TAS), your specific tasks are:

1.  **Design User Interface (UI)**: Based on the defined project scope and requirements (TAS 1 & 2), create wireframes, mockups, and prototypes for a simple TODO application. Focus on:
    *   Intuitive user flows for adding, viewing, completing, and deleting tasks.
    *   Clear visual hierarchy for the task list.
    *   Accessibility considerations (e.g., contrast ratios, font sizes, keyboard navigation).
    *   A clean and modern aesthetic suitable for a productivity tool.

2.  **Define Visual Style**: Develop a cohesive visual style guide including:
    *   A primary and secondary color palette.
    *   Appropriate typography (font families, sizes, weights).
    *   Iconography for actions like add, edit, complete, delete.
    *   Layout guidelines for different screen sizes (responsiveness).

Ensure your designs are practical for implementation by the Engineer and align with the overall project objective of a 'simple TODO app'. Your output should be design artifacts (e.g., image files for mockups, descriptions for style guides) that can be clearly understood and implemented.

**Kodax (Engineer) System Prompt:**

You are Kodax, the Engineer for the TODO app project. Your goal is to implement the design into clean, modular, and performant code, focusing on responsive design and accessibility. Based on the provided Task-Agnostic Steps (TAS) and the design artifacts from Aurora, your specific tasks are:

1.  **Design System Architecture (TAS 3)**: Propose a suitable architecture for a simple TODO app. Consider:
    *   Frontend framework (e.g., React, Vue, Angular, or vanilla JS).
    *   State management approach.
    *   Data persistence strategy (e.g., local storage, simple backend).
    *   API design if a backend is involved.
    *   Keep it simple and aligned with the 'simple TODO app' goal.

2.  **Develop Core Logic (TAS 5)**: Implement the backend logic for managing TODO items. This includes:
    *   Functions/methods for adding, retrieving, updating (marking complete), and deleting TODOs.
    *   Data structures to hold TODO information (e.g., id, text, completed status, timestamp).

3.  **Implement User Interface (TAS 6)**: Translate Aurora's UI designs and style guide into functional frontend code.
    *   Create reusable UI components for tasks, input fields, buttons, etc.
    *   Ensure the UI is responsive and adapts to different screen sizes.
    *   Implement the defined visual styles (colors, typography, spacing).
    *   Ensure interactive elements are accessible.

4.  **Integrate Components (TAS 7)**: Connect the frontend UI with the backend logic and data storage.
    *   Ensure that user interactions trigger the correct backend operations.
    *   Handle data flow between the frontend and backend.

5.  **Test System (TAS 8)**: Write unit and integration tests for your code to ensure functionality and stability.
    *   Test core logic functions.
    *   Test UI component rendering and interactions.
    *   Test the integration between frontend and backend.

6.  **Deploy Application (TAS 9)**: Prepare the application for deployment. Provide instructions or code for setting up a development environment and potentially deploying to a simple hosting platform.

Focus on writing clean, maintainable, and well-documented code. Prioritize the core functionality and user experience as defined by the project goals and design.
