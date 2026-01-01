import pytest
from t20.core.parsing import KickLangParser

def test_parse_simple_plan():
    text = """
rolePlanner PLAN SimplePlan
Stage1 action1 param1
Stage2 action2 param2
"""
    plan = KickLangParser.parse(text)
    
    assert plan.high_level_goal == "Execute plan SimplePlan"
    assert len(plan.tasks) == 2
    assert plan.tasks[0].id == "Stage1"
    assert plan.tasks[0].description == "action1 param1"
    assert plan.tasks[0].condition is None

def test_parse_nested_plan():
    text = """
rolePlanner PLAN NestedPlan
Stage1 action1
Stage2 roleSubPlanner PLAN SubPlan
"""
    plan = KickLangParser.parse(text)
    
    assert len(plan.tasks) == 2
    assert plan.tasks[1].id == "Stage2"
    assert plan.tasks[1].role == "roleSubPlanner"

def test_parse_with_params():
    text = """
roleMetaCognito PLAN MetaPlan GranularityFine HorizonShort
Stage1 action1
"""
    plan = KickLangParser.parse(text)
    
    assert "GranularityFine" in plan.high_level_goal
    assert plan.metadata["raw_params"] == "GranularityFine HorizonShort"
    assert "GranularityFine" in plan.metadata["tags"]

def test_parse_conditionals():
    text = """
rolePlanner PLAN ConditionalPlan
StageStart action0
IF tensionHigh
  StageTense actionCreateTension
  StageRun roleActor RUN Away
ELSE
  StageRelax actionChill
END
StageEnd actionFinish
"""
    plan = KickLangParser.parse(text)
    
    assert len(plan.tasks) == 5
    assert plan.tasks[1].condition == "tensionHigh"
    assert plan.tasks[2].condition == "tensionHigh"
    assert plan.tasks[3].condition == "NOT (tensionHigh)"

def test_parse_structured_actions():
    text = """
rolePlanner PLAN ActionPlan
Stage1 FIND EntityContext context
Stage2 roleBuilder EXECUTE Build Target
Stage3 roleTester TEST All
"""
    plan = KickLangParser.parse(text)
    
    # Stage1
    assert plan.tasks[0].id == "Stage1"
    assert plan.tasks[0].action_verb == "FIND"
    assert plan.tasks[0].action_params == ["EntityContext", "context"]
    
    # Stage2
    assert plan.tasks[1].id == "Stage2"
    assert plan.tasks[1].role == "roleBuilder"
    assert plan.tasks[1].action_verb == "EXECUTE"
    assert plan.tasks[1].action_params == ["Build", "Target"]

    # Stage3
    assert plan.tasks[2].id == "Stage3"
    assert plan.tasks[2].role == "roleTester"
    assert plan.tasks[2].action_verb == "TEST"
    assert plan.tasks[2].action_params == ["All"]
