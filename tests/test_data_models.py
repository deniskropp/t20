import sys
import os

# Add the project root to sys.path so we can import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

try:
    from data_models.kicklang_schemas import Component, KickLangDefinition
    from data_models.artifact_schemas import Artifact, ArtifactFile
    print("Successfully imported data models.")
except ImportError as e:
    print(f"Failed to import data models: {e}")
    sys.exit(1)

def test_kicklang_schemas():
    print("\nTesting KickLang Schemas...")
    try:
        # Create a valid KickLangDefinition
        kl_def = KickLangDefinition(
            syntax_version="1.0",
            commands=["print", "scan"],
            parameters={"verbose": True},
            metadata={"author": "User"}
        )
        print("  - KickLangDefinition instantiated successfully.")

        # Create a valid Component
        comp = Component(
            name="TestComponent",
            description="A test component",
            status="Implemented",
            kicklang_definition=kl_def
        )
        print("  - Component instantiated successfully.")
        
        # Test required fields
        try:
            Component(description="Missing name")
            print("  - FAILED: Component allowed missing 'name'.")
        except Exception:
            print("  - PASSED: Component enforced required 'name'.")

    except Exception as e:
        print(f"  - Error in KickLang Schemas test: {e}")

def test_artifact_schemas():
    print("\nTesting Artifact Schemas...")
    try:
        # Create a valid ArtifactFile
        file = ArtifactFile(
            path="src/main.py",
            content="print('Hello')"
        )
        print("  - ArtifactFile instantiated successfully.")

        # Create a valid Artifact
        artifact = Artifact(
            system_task_id="T-99",
            generated_by_agent_id=1,
            output_summary="Generated code",
            files=[file]
        )
        print("  - Artifact instantiated successfully.")

        # Test required fields
        try:
            Artifact(generated_by_agent_id=1)
            print("  - FAILED: Artifact allowed missing 'system_task_id'.")
        except Exception:
            print("  - PASSED: Artifact enforced required 'system_task_id'.")

    except Exception as e:
        print(f"  - Error in Artifact Schemas test: {e}")

if __name__ == "__main__":
    test_kicklang_schemas()
    test_artifact_schemas()
