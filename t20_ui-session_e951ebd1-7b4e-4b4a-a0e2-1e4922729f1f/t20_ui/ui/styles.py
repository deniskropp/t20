# Stylesheets and theme definitions

# Using the color palette from the design concept
PRIMARY_COLOR = "#1A237E"    # Indigo 900
SECONDARY_COLOR = "#424242"   # Grey 700
ACCENT_COLOR = "#00ACC1"     # Cyan 500 (Teal)
ACCENT_HOVER_COLOR = "#00838F" # Darker Teal for hover
TEXT_LIGHT = "#F5F5F5"       # Off-white
TEXT_DARK = "#212121"        # Dark Grey
ERROR_COLOR = "#FF0000"
SUCCESS_COLOR = "#00FF00"

# Font family
FONT_FAMILY = "Roboto, Open Sans, Lato"

MAIN_STYLESHEET = f"""
QWidget {{
    background-color: {SECONDARY_COLOR};
    color: {TEXT_LIGHT};
    font-family: "{FONT_FAMILY}";
    font-size: 11pt;
}}

QMainWindow {{
    background-color: {SECONDARY_COLOR};
    color: {TEXT_LIGHT};
}}

QSplitter::handle {{
    background-color: {PRIMARY_COLOR};
    width: 3px;
}}

QLabel {{
    color: {TEXT_LIGHT};
    font-weight: bold;
}}

QPushButton {{
    background-color: {ACCENT_COLOR};
    color: {TEXT_DARK};
    border: none;
    padding: 8px 15px;
    border-radius: 4px;
    font-weight: bold;
}}

QPushButton:hover {{
    background-color: {ACCENT_HOVER_COLOR};
}}

QPushButton#runButton {{
    background-color: {SUCCESS_COLOR};
    color: {TEXT_DARK};
    font-size: 14pt;
    padding: 10px;
}}

QPushButton#runButton:hover {{
    background-color: #00CC00;
}}

QTextEdit, QLineEdit, QComboBox, QSpinBox {{
    background-color: #37474F; /* Darker Grey */
    color: {TEXT_LIGHT};
    border: 1px solid #616161;
    border-radius: 4px;
    padding: 5px;
}}

QTextEdit:read-only {{
    background-color: #303030; /* Slightly different dark for read-only */
    border: 1px solid #555555;
}}

QProgressBar {{
    border: 2px solid {ACCENT_COLOR};
    border-radius: 5px;
    text-align: center;
    color: {TEXT_LIGHT};
}}

QProgressBar::chunk {{
    background-color: {ACCENT_COLOR};
    width: 20px;  /* adjust as needed */
    margin: 0.5px;
}}

QListWidget {{
    border: 1px solid #616161;
    border-radius: 4px;
    padding: 5px;
    background-color: #37474F;
}}

QListWidget::item {{
    padding: 5px;
}}

QListWidget::item:selected {{
    background-color: {ACCENT_COLOR};
    color: {TEXT_DARK};
}}

/* Specific overrides for status log */
#statusLogWidget QTextEdit {{ /* Assuming StatusLogWidget has objectName 'statusLogWidget' if needed */ 
    font-family: "{FONT_FAMILY}";
    font-size: 10pt;
    background-color: #263238; /* Blue Grey 900 */
    border: 1px solid #455A64;
}}

/* Specific overrides for output display */
#outputDisplayWidget QTextEdit {{ /* Assuming OutputDisplayWidget has objectName 'outputDisplayWidget' if needed */ 
    font-family: "{FONT_FAMILY}";
    font-size: 11pt;
    background-color: #263238; /* Blue Grey 900 */
    border: 1px solid #455A64;
}}

"""
