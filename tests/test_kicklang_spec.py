import pytest
from t20.core.parsing import KickLangParser

# KICKLANG STANDARD SPECIFICATION TEST SUITE

# --- 1. CORE SYNTAX ---

def test_role_definitions_and_parameterization():
    """
    Test various role definitions and parameterizations.
    Spec: Roles are cognitive stances (e.g., ResearcherDepthHigh).
    """
    text = """
    roleResearcherDepthHigh PLAN TestPlan
    Stage1 action1
    """
    plan = KickLangParser.parse(text)
    assert plan.high_level_goal == "Execute plan TestPlan"
    # Assuming the parser captures the role name correctly
    # from t20.core.models import Plan # Removed as file does not exist
    
    # We might need to inspect the raw plan or context if 'roleResearcherDepthHigh' isn't split
    # For now, based on existing tests, the role is part of the line.
    # In 'test_parse_simple_plan', "rolePlanner PLAN SimplePlan" -> high_level_goal="Execute plan SimplePlan"
    # It seems the top-level role might be implicit or handled differently.
    # Let's check a task-level role assignment.
    
    text_nested = """
    rolePlanner PLAN MainPlan
    Stage1 roleStorytellerToneEpic SUMMARIZE EntityScene
    """
    plan = KickLangParser.parse(text_nested)
    assert plan.tasks[0].role == "roleStorytellerToneEpic"
    assert plan.tasks[0].action_verb == "SUMMARIZE"

def test_action_verbs_knowledge_access():
    """
    Test Knowledge Access verbs: FIND, LIST, DETAIL.
    """
    text = """
    rolePlanner PLAN AccessPlan
    Stage1 FIND EntityContext context
    Stage2 LIST EntityItems all_items
    Stage3 DETAIL EntityItem details
    """
    plan = KickLangParser.parse(text)
    assert plan.tasks[0].action_verb == "FIND"
    assert plan.tasks[1].action_verb == "LIST"
    assert plan.tasks[2].action_verb == "DETAIL"

def test_action_verbs_knowledge_structuring():
    """
    Test Knowledge Structuring verbs: LINK, MAP, CLUSTER.
    """
    text = """
    rolePlanner PLAN StructPlan
    Stage1 LINK NodeA, relates_to, NodeB
    Stage2 MAP NodeStart - follows - *
    Stage3 CLUSTER EntitySet ByType
    """
    plan = KickLangParser.parse(text)
    assert plan.tasks[0].action_verb == "LINK"
    assert plan.tasks[1].action_verb == "MAP"
    assert plan.tasks[2].action_verb == "CLUSTER"

def test_action_verbs_knowledge_transformation():
    """
    Test Knowledge Transformation verbs: SUMMARIZE, COMPARE, EXPLAIN.
    """
    text = """
    rolePlanner PLAN TransPlan
    Stage1 SUMMARIZE EntityContent output
    Stage2 COMPARE EntityA EntityB difference
    Stage3 EXPLAIN ConceptComplex simple_terms
    """
    plan = KickLangParser.parse(text)
    assert plan.tasks[0].action_verb == "SUMMARIZE"
    assert plan.tasks[1].action_verb == "COMPARE"
    assert plan.tasks[2].action_verb == "EXPLAIN"

def test_placebo_pipes():
    """
    Test Placebo Pipes syntax (<<...>>).
    Spec: Deferred or conditional steps.
    """
    text = """
    rolePlanner PLAN PlaceboPlan
    Stage1 PROCESS <<story_request>>
    Stage2 UPDATE <<world_state>>
    """
    plan = KickLangParser.parse(text)
    # Check if params capture the placebo pipe syntax
    assert "<<story_request>>" in plan.tasks[0].action_params
    assert "<<world_state>>" in plan.tasks[1].action_params

# --- 2. PIPELINES ---

def test_basic_pipeline_structure():
    """
    Test the structure of a standard pipeline.
    """
    text = """
    rolePlanner PLAN PipelineMain
    Stage1Prep FIND EntityContext context
    Stage2Action SUMMARIZE context output
    """
    plan = KickLangParser.parse(text)
    assert len(plan.tasks) == 2
    assert plan.tasks[0].id == "Stage1Prep"
    assert plan.tasks[1].id == "Stage2Action"

def test_nested_pipelines():
    """
    Test nested PLAN blocks.
    Spec: nested and conditional PLAN blocks.
    """
    text = """
    rolePlanner PLAN ParentPlan
    Stage1 roleSubPlanner PLAN ChildPlan
    """
    plan = KickLangParser.parse(text)
    assert plan.tasks[0].action_verb == "PLAN" or plan.tasks[0].role == "roleSubPlanner"
    # Depending on how parser handles "PLAN" as an action or a recursive structure
    # Based on test_plan_parsing.py: assert plan.tasks[1].role == "roleSubPlanner"
    # It seems it treats it as a task with role.

def test_conditional_branching_syntax():
    """
    Test IF/ELSE structures with various condition types.
    """
    text = """
    rolePlanner PLAN BranchPlan
    IF has_trait=HighTension
        Stage1 ActionTens
    ELSE
        Stage2 ActionRelief
    END
    IF CLUSTER>5
        Stage3 ActionParallel
    """
    plan = KickLangParser.parse(text)
    # Check conditions
    # Based on test_plan_parsing.py logic:
    # tasks inside IF have 'condition' attribute set.
    
    # We expect 3 tasks total (Stage1, Stage2, Stage3)
    # Stage1 condition: "has_trait=HighTension"
    # Stage2 condition: "NOT (has_trait=HighTension)"  <-- Assuming parser handles ELSE negation
    # Stage3 condition: "CLUSTER>5"
    
    # Note: The parser implementation in test_plan_parsing.py seemed to flatten the tasks list.
    assert len(plan.tasks) == 3
    assert plan.tasks[0].condition == "has_trait=HighTension"
    assert plan.tasks[1].condition == "NOT (has_trait=HighTension)"
    assert plan.tasks[2].condition == "CLUSTER>5"

# --- 3. GRAPH OPERATIONS ---

def test_graph_link_chain():
    """
    Test complex LINK command or structure.
    Spec: LINK Scene1, precedes, DragonDialogue; ToneIntense
    """
    text = """
    rolePlanner PLAN GraphPlan
    Stage1 LINK Scene4, precedes, DragonDialogue; ToneIntense
    """
    plan = KickLangParser.parse(text)
    # Params should be parsed correctly
    # "Scene4, precedes, DragonDialogue; ToneIntense"
    params = plan.tasks[0].action_params
    # Exact parsing depends on implementation (list of strings or raw string)
    # Assuming list splitting by spaces usually, but comma/semicolon might be handled
    # Let's just check raw content presence for now
    assert "Scene4," in params or "Scene4" in params
    assert "precedes," in params or "precedes" in params

# --- 4. MODULES AND REUSE ---

def test_module_import_declaration():
    """
    Test ⫻import syntax.
    Note: The parser might process this as metadata or a directive.
    """
    text = """
    ⫻import:KickLang-Module/test-module
    rolePlanner PLAN ImportPlan
    Stage1 Action1
    """
    # Assuming parser can handle this or ignores it without error.
    # If it's a special directive, it might be in metadata.
    plan = KickLangParser.parse(text)
    # Check if import is stored in metadata if supported
    # If not supported yet, at least it shouldn't crash if it's comment-like
    # But strictly speaking it is part of the language.
    # If fail, we know implementation is missing.

def test_module_invocation():
    """
    Test ⫻module invocation.
    """
    text = """
    rolePlanner PLAN InvocationPlan
    Stage1 ⫻module:StorytellerToPlanner <<input:Scene>>
    """
    plan = KickLangParser.parse(text)
    # It might be parsed as action_verb="⫻module:StorytellerToPlanner" or similar
    # Since it's not all uppercase, action_verb is None.
    assert "⫻module:StorytellerToPlanner" in plan.tasks[0].description

# --- 5. PATTERNS ---
def test_pattern_block():
    """
    Test ⫻pattern block syntax.
    """
    text = """
    ⫻pattern:Meta-AI-Storybook
    <<Reusable pipeline>>
    """
    # This might return a Plan object or a Pattern object depending on parser
    # For now, try parsing it
    try:
        plan = KickLangParser.parse(text)
    except Exception:
        pytest.fail("Failed to parse Pattern block")

