import logging
import sys

# Configure logging to stdout
logging.basicConfig(level=logging.INFO, format='%(message)s')

def test_ast_movement():
    print("Testing imports from t20sdk.lang.ast...")
    try:
        from t20sdk.lang.ast import Step, Plan, Pipeline
        print("✅ Successfully imported Step, Plan, Pipeline from t20sdk.lang.ast")
    except ImportError as e:
        print(f"❌ Failed to import from t20sdk.lang.ast: {e}")
        sys.exit(1)

def test_backward_compatibility():
    print("Testing backward compatibility imports from t20sdk.lang.syntax...")
    try:
        from t20sdk.lang.syntax import Step, Plan, Pipeline
        print("✅ Successfully imported Step, Plan, Pipeline from t20sdk.lang.syntax")
    except ImportError as e:
        print(f"❌ Failed to import from t20sdk.lang.syntax: {e}")
        sys.exit(1)

def test_object_creation():
    print("Testing object creation...")
    try:
        from t20sdk.lang.ast import Step, Plan, Pipeline
        from t20sdk.lang.spec import Placebo
        
        step = Step(name="test_step", action=Placebo(marker="test"))
        plan = Plan(name="test_plan")
        plan.add_step(step)
        pipeline = Pipeline(name="test_pipeline", root_plan=plan)
        
        print(f"✅ Created Pipeline: {pipeline.name}")
        print(plan.describe())
    except Exception as e:
        print(f"❌ Failed to create objects: {e}")
        sys.exit(1)

def test_if_block():
    print("Testing IfBlock...")
    try:
        from t20sdk.lang.ast import Step, Plan, IfBlock
        from t20sdk.lang.spec import Placebo
        
        step_true = Step(name="true_step", action=Placebo(marker="true"))
        step_false = Step(name="false_step", action=Placebo(marker="false"))
        
        if_block = IfBlock(
            condition="x > 5",
            then_branch=[step_true],
            else_branch=[step_false]
        )
        
        plan = Plan(name="conditional_plan")
        plan.add_step(if_block)
        
        desc = plan.describe()
        print(desc)
        if "IF x > 5" in desc and "ELSE" in desc:
            print("✅ IfBlock described correctly")
        else:
            print("❌ IfBlock description missing components")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Failed to use IfBlock: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_ast_movement()
    # test_backward_compatibility() - syntax.py deleted
    test_object_creation()
    test_if_block()
