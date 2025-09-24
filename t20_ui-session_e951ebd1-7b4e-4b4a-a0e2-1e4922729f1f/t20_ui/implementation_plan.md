# Technical Implementation Plan: Multi-Agent System UI (PyQt6)

## 1. Project Structure

The PyQt6 application will follow a modular structure to ensure maintainability and scalability. The proposed directory structure is as follows:

```
t20_ui/
├── __init__.py
├── main.py                 # Application entry point
├── ui/
│   ├── __init__.py
│   ├── main_window.py      # Main application window (QMainWindow)
│   ├── widgets/
│   │   ├── __init__.py
│   │   ├── agent_config_widget.py # Widget for configuring agents and runtime parameters
│   │   ├── input_output_widget.py # Widget for task input and final output display
│   │   ├── status_log_widget.py   # Widget for real-time status and logs
│   │   ├── progress_widget.py     # Widget for displaying task progress
│   │   └── artifact_browser_widget.py # Widget for browsing and previewing artifacts
│   └── styles/
│       ├── __init__.py
│       └── theme.qss       # Qt Style Sheets for theming and responsiveness
├── runtime/
│   ├── __init__.py
│   ├── executor.py         # Module to interact with the T20 runtime package
│   └── signal_handler.py   # Handles signals from the runtime process
├── cli/
│   ├── __init__.py
│   └── argument_parser.py  # Handles parsing of sysmain CLI arguments
├── utils/
│   ├── __init__.py
│   └── helpers.py          # Utility functions
└── tests/
    ├── __init__.py
    ├── ui/
    │   ├── __init__.py
    │   └── test_widgets.py     # Unit tests for UI components
    └── runtime/
        ├── __init__.py
        └── test_executor.py    # Integration tests for runtime interaction
```

## 2. Core Components Implementation

Key UI components will be implemented using PyQt6 classes:

*   **`QMainWindow` (`main_window.py`)**: The main application window, serving as the central hub. It will manage the layout of other widgets using `QVBoxLayout` and `QSplitter` for resizable sections.
*   **`QWidget`**: Base class for custom widgets.
*   **`QPushButton`**: Used for actions like 'Run Task', 'Browse Artifacts', etc.
*   **`QLineEdit` / `QTextEdit`**: For user input of the task goal and description. `QTextEdit` will also be used for displaying detailed agent outputs and logs.
*   **`QProgressBar`**: To visually represent the progress of agent execution.
*   **`QListWidget` / `QTreeView`**: For displaying lists of available agents, runtime configurations, and artifacts.
*   **`QComboBox`**: For selecting orchestrators, models, etc.
*   **`QSplitter`**: To allow users to resize different sections of the UI (e.g., input/output, logs).
*   **`QProcess`**: Crucial for running the `t20-system` as a subprocess without blocking the UI event loop.

**Styling**: Qt Style Sheets (`.qss` files) will be used for consistent theming, responsiveness (adapting to different window sizes), and accessibility (ensuring sufficient color contrast).

## 3. Runtime Integration Strategy

Integration with the T20 runtime package will be managed by the `runtime/executor.py` module.

*   **Triggering Agent Execution**: A `QPushButton` (e.g., 'Run Task') in the UI will trigger a method in `runtime/executor.py`. This method will construct the `t20-system` command-line arguments based on user input and selected configurations.
*   **`QProcess` for Subprocess**: `QProcess` will be instantiated to execute the `t20-system` command. This allows the UI to remain responsive while the runtime executes.
*   **Real-time Status and Outputs**: `QProcess` provides signals (`readyReadStandardOutput`, `readyReadStandardError`, `stateChanged`) that will be connected to slots in `runtime/signal_handler.py`. These slots will parse the output streams (stdout/stderr) from the `t20-system` subprocess.
    *   Log messages will be parsed and displayed in the `status_log_widget.py`.
    *   Progress indicators (if provided by the runtime) will update the `progress_widget.py`.
    *   The final output will be captured and displayed in the `input_output_widget.py`.
*   **Asynchronous Operations**: The use of `QProcess` and PyQt's signal/slot mechanism inherently handles asynchronous operations. The main UI thread is not blocked by the subprocess execution, ensuring a smooth user experience.

## 4. CLI Argument Handling

*   **`cli/argument_parser.py`**: This module will utilize Python's `argparse` library to define and parse arguments expected by `sysmain`. 
*   **Integration**: 
    1.  When the application starts, the `main.py` script will parse any initial CLI arguments provided to the PyQt application itself (e.g., `--theme`, `--config-file`).
    2.  When the 'Run Task' button is pressed, the UI will gather configuration from its widgets (orchestrator, model, rounds, files) and combine them with the task description to form the arguments passed to the `t20-system` subprocess via `QProcess`. This ensures that `sysmain` arguments are correctly translated and executed.

## 5. Event Loop Management

*   **`QApplication`**: The `main.py` script will instantiate `QApplication`, which is responsible for managing the application's event loop.
*   **Event Processing**: The event loop continuously monitors for events (user interactions, signals from subprocesses, network events, etc.) and dispatches them to the appropriate objects (widgets, slots).
*   **Responsiveness**: By running the `t20-system` subprocess using `QProcess` and handling its output via signals, the main event loop remains free to process UI events, ensuring the application remains responsive.

## 6. Accessibility Considerations

*   **Keyboard Navigation**: Ensure all interactive elements (`QPushButton`, `QLineEdit`, `QComboBox`, etc.) are focusable and navigable using the keyboard (Tab, Shift+Tab, Enter, Space). Use `QWidget.setFocusPolicy()` appropriately.
*   **Screen Reader Compatibility**: Use clear and descriptive labels for all widgets (`QLabel.setText()`, `QToolTip.set` for tooltips). Ensure text in log and output areas is accessible.
*   **Color Contrast**: Adhere to WCAG AA standards for color contrast ratios in the default stylesheets. Provide high-contrast theme options if possible.
*   **Focus Indicators**: Implement clear visual indicators for the currently focused widget.
*   **Layout**: Use logical layouts (`QVBoxLayout`, `QHBoxLayout`, `QGridLayout`) that remain understandable when navigated via keyboard or screen reader.

## 7. Testing Strategy

*   **Unit Tests (`tests/ui/test_widgets.py`)**: Test individual UI components in isolation using `pytest` and PyQt's testing utilities. Verify widget rendering, signal emission, and basic interactions.
*   **Integration Tests (`tests/runtime/test_executor.py`)**: Test the interaction between the UI and the T20 runtime. This involves:
    *   Mocking `QProcess` or running `t20-system` in a controlled environment.
    *   Verifying that commands are correctly constructed and executed.
    *   Checking that output signals are correctly received and processed.
    *   Ensuring the UI updates appropriately based on runtime feedback.
*   **End-to-End Tests**: Manual or automated testing of the complete user flow, from inputting a task to viewing the final output and artifacts.
*   **Accessibility Testing**: Manual testing using keyboard navigation and screen readers (e.g., NVDA, VoiceOver) to verify compliance with accessibility guidelines.
*   **Performance Testing**: Monitor UI responsiveness and resource usage during typical and intensive runtime operations.