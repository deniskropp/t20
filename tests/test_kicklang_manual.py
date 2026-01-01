import logging
import sys
from t20.lang import (
    Role, Action, ActionType, Placebo,
    Planner, Researcher, Storyteller,
    Step, Plan, Pipeline, PlanExecutor
)

# Configure logging to stdout
logging.basicConfig(level=logging.INFO, format='%(message)s')

def test_kicklang_pipeline():
    print("--- Defining Roles ---")
    role_planner = Planner(granularity="coarse")
    role_sub_planner = Planner(name="SubPlanner", granularity="fine")
    role_researcher = Researcher()
    
    print(f"Roles: {role_planner}, {role_sub_planner}, {role_researcher}")

    print("\n--- Defining Sub-Pipeline ---")
    sub_plan = Plan(name="PipelineSub")
    sub_plan.add_step(Step(
        name="SubStage1",
        role=role_researcher,
        action=Action(verb=ActionType.FIND, target="Specific Details", parameters={"query": "deep search"}),
        output_var="sub_output"
    ))

    print("\n--- Defining Main Pipeline ---")
    main_plan = Plan(name="PipelineMain")
    
    # Stage 1: Prep
    main_plan.add_step(Step(
        name="Stage1Prep",
        role=role_planner,
        action=Action(verb=ActionType.FIND, target="EntityContext"),
        output_var="context"
    ))
    
    # Stage 2: Nested (simulating the 'roleSubPlanner PLAN PipelineSub context' line)
    main_plan.add_step(Step(
        name="Stage2Nested",
        role=role_sub_planner,
        action=Action(
            verb=ActionType.PLAN, 
            target="PipelineSub", 
            parameters={"sub_plan": sub_plan, "context": "context"}
        ),
        output_var="nested_result"
    ))

    # Stage 3: Synth
    main_plan.add_step(Step(
        name="Stage3Synth",
        role=Storyteller(tone="professional"),
        action=Action(verb=ActionType.SUMMARIZE, target="PipelineSub"),
        input_var="nested_result",
        output_var="final_output"
    ))

    pipeline = Pipeline(name="ExamplePipeline", root_plan=main_plan)
    
    print("\n--- Describing Pipeline ---")
    print(main_plan.describe())

    print("\n--- Executing Pipeline ---")
    executor = PlanExecutor()
    executor.execute_pipeline(pipeline)

if __name__ == "__main__":
    test_kicklang_pipeline()
