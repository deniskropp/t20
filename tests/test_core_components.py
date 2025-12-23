import sys
import os

# Add project root to sys.path
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
sys.path.insert(0, root_dir)

try:
    from config.system_governance import SystemGovernance
    from knowledge_graph.interface import KnowledgeGraphInterface
    from data_models.kicklang_schemas import Component
    print("Successfully imported core components.")
except ImportError as e:
    print(f"Failed to import core components: {e}")
    sys.exit(1)

def test_system_governance():
    print("\nTesting System Governance...")
    
    # Test Status Flow
    current = "Defined"
    expected_next = "Designed"
    next_status = SystemGovernance.get_next_allowed_status(current)
    if next_status == expected_next:
        print(f"  - PASSED: Correct next status for '{current}' is '{next_status}'")
    else:
        print(f"  - FAILED: Expected '{expected_next}', got '{next_status}'")

    # Test Invalid Transition
    if not SystemGovernance.is_transition_valid("Defined", "Verified"):
        print("  - PASSED: Correctly rejected skip from 'Defined' to 'Verified'")
    else:
        print("  - FAILED: Allowed invalid skip transition")

def test_knowledge_graph_interface():
    print("\nTesting Knowledge Graph Interface...")
    kg = KnowledgeGraphInterface()
    
    # Test Adding Component
    comp = Component(name="TestComp", description="Desc")
    if kg.add_component(comp):
        print("  - PASSED: Added component successfully")
    else:
        print("  - FAILED: Could not add component")

    # Test Getting Component
    fetched = kg.get_component("TestComp")
    if fetched and fetched.name == "TestComp":
        print("  - PASSED: Retrieved component successfully")
    else:
        print("  - FAILED: Could not retrieve component")

    # Test Updating Status (Valid)
    if kg.update_component_status("TestComp", "Designed"):
        print("  - PASSED: Updated status to 'Designed'")
    else:
        print("  - FAILED: Failed to update status to 'Designed'")

    # Test Updating Status (Invalid)
    if not kg.update_component_status("TestComp", "Verified"): # Skipping Implemented
        print("  - PASSED: Correctly blocked invalid status update to 'Verified'")
    else:
        print("  - FAILED: Allowed invalid status update")

if __name__ == "__main__":
    test_system_governance()
    test_knowledge_graph_interface()
