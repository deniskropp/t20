import pytest
from t20.core.parsing import KickLangParser
from t20.core.custom_types import Task

def test_nested_plan_parsing_details():
    """
    Verifies that a 'PLAN' keyword in a task description is correctly preserved
    and accessible, allowing the runtime to identify it as a nested plan directive.
    """
    text = """
roleMain PLAN MainProject
Stage1 roleSub PLAN SubComponent
"""
    plan = KickLangParser.parse(text)
    
    assert len(plan.tasks) == 1
    task = plan.tasks[0]
    
    assert task.id == "Stage1"
    assert task.role == "roleSub"
    assert task.description == "PLAN SubComponent"
    # Verify that we can identify it as a nested plan call via string check
    assert task.description.startswith("PLAN ")
    assert task.description.split()[1] == "SubComponent"

def test_nested_plan_extraction():
    """
    Verifies that we can extract the sub-plan name from the description.
    """
    description = "PLAN DatabaseSchema"
    if description.startswith("PLAN "):
        sub_plan_name = description[5:].strip()
        assert sub_plan_name == "DatabaseSchema"
