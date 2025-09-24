## T20 Multi-Agent System UI Design Concept

This document outlines the UI design concept for the T20 Multi-Agent System, focusing on creating an intuitive, accessible, and visually appealing interface using PyQt6.

### 1. Conceptual Layout

The main UI window will adopt a modern, three-panel layout:

*   **Left Panel (Control & Configuration):**
    *   **Top Section:** Input field for the primary task goal.
    *   **Middle Section:** Configuration options for the runtime (e.g., selecting orchestrator, model, number of rounds). This section will dynamically adapt based on CLI arguments or default settings.
    *   **Bottom Section:** A prominent 'Run Task' button to initiate the multi-agent process.
*   **Center Panel (Status & Progress):**
    *   **Top Section:** A real-time log view displaying agent activities, messages, and system events. This will be a scrollable text area.
    *   **Bottom Section:** A progress indicator (e.g., a progress bar or a series of status icons) visualizing the overall task completion and the current agent's progress.
*   **Right Panel (Output & Artifacts):**
    *   **Top Section:** Displays the final output or results of the task. This could be a text area, a table, or a structured view depending on the output type.
    *   **Bottom Section:** A file explorer or list view to browse and access generated artifacts from specific agent runs within a session. Allows for downloading or opening artifacts.

*   **Top Menu Bar (Optional but Recommended):**
    *   `File`: New Session, Open Session, Exit.
    *   `Edit`: Preferences (e.g., theme, font size).
    *   `View`: Toggle panels, Reset layout.
    *   `Help`: About, Documentation.

### 2. Key UI Elements

*   **Task Input (`QLineEdit` or `QTextEdit`):** A clear, prominent area for users to enter their primary goal.
*   **Configuration Widgets (`QComboBox`, `QSpinBox`, `QLineEdit`, `QCheckBox`):** Used for selecting orchestrators, models, setting rounds, and other runtime parameters. These should be grouped logically.
*   **Action Buttons (`QPushButton`):**
    *   'Run Task': Starts the agent execution.
    *   'Stop/Cancel Task': Halts the ongoing process.
    *   'Clear Output/Log': Resets the display areas.
    *   Buttons for managing artifacts (e.g., 'Save', 'Open').
*   **Progress Indicators (`QProgressBar`, `QMovie` for spinners):** Visual feedback on task execution status.
*   **Log/Output Display (`QTextEdit` with rich text support or `QTableView`):** For displaying detailed logs and final results. Should support scrolling and potentially syntax highlighting for code outputs.
*   **Status Bar (Bottom of window):** Displays brief status messages, current agent activity, or connection status.
*   **Tooltips and Status Tips:** Provide contextual help for buttons and controls.

### 3. Visual Theme Concept

*   **Color Palette:**
    *   **Primary:** A deep, professional blue (`#1A237E` - Indigo 900) for backgrounds or accents, conveying stability and trust.
    *   **Secondary:** A balanced grey (`#424242` - Grey 700) for secondary panels or text, ensuring readability.
    *   **Accent:** A vibrant, yet not overwhelming, teal (`#00ACC1` - Cyan 500) or a warm orange (`#FF8F00` - Amber 700) for interactive elements like buttons, progress bars, and highlights, drawing user attention.
    *   **Text:** Off-white (`#F5F5F5`) on dark backgrounds, and a dark grey (`#212121`) on lighter backgrounds for maximum contrast.
    *   **Status Colors:** Green for success, Yellow for warning, Red for error.
*   **Typography:**
    *   **Font Family:** A clean, sans-serif font like 'Roboto', 'Open Sans', or 'Lato' for UI elements and body text to ensure excellent readability on screens.
    *   **Font Sizes:** Use a clear hierarchy: 16-18pt for titles, 12-14pt for body text, 10-11pt for labels and secondary information.
*   **Accessibility:**
    *   **Contrast Ratio:** Ensure all text and interactive elements meet WCAG AA standards (minimum 4.5:1 for normal text, 3:1 for large text).
    *   **Keyboard Navigation:** All interactive elements must be navigable and operable using the keyboard.
    *   **Scalability:** Allow users to adjust font sizes and UI scaling through preferences.
    *   **Clear Focus Indicators:** Ensure elements have distinct visual indicators when they are in focus.

### 4. User Flow Outline

1.  **Launch Application:** User launches the PyQt6 application. The UI loads with default settings or settings parsed from `sysmain` CLI arguments.
2.  **Define Goal:** User enters the high-level task goal into the input field in the Control Panel.
3.  **Configure Task (Optional):** User adjusts runtime parameters (orchestrator, model, rounds) in the Control Panel if needed.
4.  **Initiate Task:** User clicks the 'Run Task' button.
5.  **Monitor Execution:** The Status Panel updates in real-time:
    *   The log area shows messages from the runtime and agents.
    *   The progress indicator updates to show task progression.
6.  **View Results:** Once execution is complete:
    *   The final output appears in the Output Panel.
    *   Any generated artifacts are listed in the Artifacts section of the Output Panel.
7.  **Interact with Artifacts:** User can browse, open, or save artifacts from the Output Panel.
8.  **New Task:** User can clear the fields and input a new goal to start another task, or use the menu to manage sessions.

This design prioritizes a clear separation of concerns, making it easy for users to understand the system's state and control its execution.