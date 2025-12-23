import logging
from t20sdk.lang import (
    Role, Action, ActionType,
    Summarizer, Analyst,
    Step, Plan, Pipeline, PlanExecutor
)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

def test_refinements():
    print("--- Testing New Roles ---")
    role_summarizer = Summarizer(brevity="extreme")
    role_analyst = Analyst(approach="statistical")
    print(f"Roles Created: {role_summarizer}, {role_analyst}")
    
    print("\n--- Testing Action Verbs ---")
    # Using new verbs from reference if any (Link, Map, etc were already there)
    action_link = Action(verb=ActionType.LINK, target="EntityA", parameters={"relation": "CAUSE", "to": "EntityB"})
    print(f"Action Created: {action_link}")

    print("\n--- Executing Mini Pipeline with New Roles ---")
    plan = Plan(name="RefinementPlan")
    plan.add_step(Step(
        name="StageAnalyze", 
        role=role_analyst, 
        action=Action(verb=ActionType.MAP, target="DataPoints"),
        output_var="mapped_data"
    ))
    plan.add_step(Step(
        name="StageSummarize", 
        role=role_summarizer, 
        action=Action(verb=ActionType.SUMMARIZE, target="mapped_data"),
        output_var="summary"
    ))
    
    pipeline = Pipeline(name="RefinementPipeline", root_plan=plan)
    executor = PlanExecutor()
    executor.execute_pipeline(pipeline)

if __name__ == "__main__":
    test_refinements()
