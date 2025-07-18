#!/bin/bash

# Create HTML file
cat << EOF > index.html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Project Plan</title>
    <style>
        body { font-family: sans-serif; margin: 20px; }
        h1 { color: #333; }
        .step { margin-bottom: 30px; border: 1px solid #eee; padding: 15px; border-radius: 5px; }
        .step h2 { margin-top: 0; color: #555; }
        .step p { margin-bottom: 10px; }
        .step ul { padding-left: 20px; }
        .step li { margin-bottom: 5px; }
        code { background-color: #f4f4f4; padding: 2px 4px; border-radius: 3px; }
    </style>
</head>
<body>
    <h1>Project Plan Steps</h1>
EOF

# Process each step
echo "$(<plan.json)" | jq -c '.plan[]' | while read -r step_data; do
    step_number=$(echo "$step_data" | jq '.step')
    task=$(echo "$step_data" | jq -r '.task')
    html_structure=$(echo "$step_data" | jq -r '.code_implementation_details.html_structure')
    css_styling=$(echo "$step_data" | jq -r '.code_implementation_details.css_styling')
    javascript_functionality=$(echo "$step_data" | jq -r '.code_implementation_details.javascript_functionality')
    accessibility_considerations=$(echo "$step_data" | jq -r '.code_implementation_details.accessibility_considerations')
    component_breakdown=$(echo "$step_data" | jq '.code_implementation_details.component_breakdown')

    echo "
    <div class=\"step\">
        <h2>Step $step_number: $task</h2>
        <p><strong>HTML Structure:</strong> $html_structure</p>
        <p><strong>CSS Styling:</strong> $css_styling</p>
        <p><strong>JavaScript Functionality:</strong> $javascript_functionality</p>
        <p><strong>Accessibility Considerations:</strong> $accessibility_considerations</p>
        <p><strong>Component Breakdown:</strong></p>
        <ul>
    " >> index.html

    echo "$component_breakdown" | jq -r 'to_entries[] | "<li>" + .key + ": " + .value + "</li>"' >> index.html

    echo "
        </ul>
    </div>
    " >> index.html
done

# Close HTML file
cat << EOF >> index.html
</body>
</html>
EOF

# Create JavaScript file
cat << EOF > script.js
// JavaScript for Project Plan Visualization

// Placeholder for dynamic functionality if needed later
console.log("Project plan script loaded.");

// Example: Function to highlight a step (not implemented in HTML structure)
function highlightStep(stepNumber) {
    console.log("Highlighting step:", stepNumber);
}
EOF

echo "Generated index.html and script.js"
