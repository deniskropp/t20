import pytest
from t20.core.custom_types import Task, Plan
from t20.core.task_manager import TaskManager, TaskStatus

def test_task_model_recursion():
    """Verify Task model supports nested subtasks."""
    subtask = Task(
        id="T-1.1", 
        description="Subtask", 
        role="Dev", 
        agent="Coder", 
        deps=[]
    )
    parent = Task(
        id="T-1", 
        description="Parent", 
        role="Lead", 
        agent="Manager", 
        deps=[],
        subtasks=[subtask]
    )
    
    assert parent.subtasks is not None
    assert len(parent.subtasks) == 1
    assert parent.subtasks[0].id == "T-1.1"

def test_task_manager_flattening():
    """Verify TaskManager correctly flattens hierarchical tasks."""
    subtask = Task(id="T-1.1", description="Sub", role="R", agent="A", deps=[])
    parent = Task(id="T-1", description="Parent", role="R", agent="A", deps=[], subtasks=[subtask])
    
    plan = Plan(high_level_goal="Test", reasoning="None", roles=[], tasks=[parent])
    
    manager = TaskManager(plan)
    
    assert "T-1" in manager.tasks
    assert "T-1.1" in manager.tasks
    assert manager.parent_map["T-1.1"] == "T-1"
    assert "T-1.1" in manager.children_map["T-1"]

def test_htn_lifecycle_flow():
    """Verify the lifecycle flow of a HTN plan."""
    # Structure:
    # T-1 (Parent) -> [T-1.1, T-1.2]
    # T-2 (Dependent on T-1)
    
    t1_1 = Task(id="T-1.1", description="Sub 1", role="R", agent="A", deps=[])
    t1_2 = Task(id="T-1.2", description="Sub 2", role="R", agent="A", deps=[]) # Independent sibling
    
    t1 = Task(id="T-1", description="Parent", role="R", agent="A", deps=[], subtasks=[t1_1, t1_2])
    t2 = Task(id="T-2", description="Follow-up", role="R", agent="A", deps=["T-1"])
    
    plan = Plan(high_level_goal="Test", reasoning="None", roles=[], tasks=[t1, t2])
    manager = TaskManager(plan)
    
    # 1. Initial State
    # T-1 is ready (no deps). T-2 is pending (dep T-1).
    # T-1.1, T-1.2 are pending (waiting for T-1 to start).
    
    ready = manager.get_ready_tasks()
    # Logic expectation: 
    # T-1 is a container. If it's ready, manager auto-starts it.
    # T-1 -> RUNNING.
    # T-1.1, T-1.2 -> Ready (parent running, they have no deps).
    # So ready list should contain T-1.1 and T-1.2.
    
    # Let's see if our logic holds.
    # T-1 is pending. _can_start(T-1) -> True (deps=[]).
    # Loop finds T-1. Has subtasks. Auto-mark T-1 RUNNING.
    # What about children? They are also PENDING.
    # _can_start(T-1.1) -> True (deps=[], parent T-1 is RUNNING).
    # So they should be picked up in the SAME loop?
    # Our loop iterates over a snapshot of pending_ids.
    # T-1 is processed. T-1.1 is also in the list? Yes.
    # If key order allows, T-1.1 might be processed after T-1.
    # Even if processed before, T-1 wasn't running yet.
    # Ideally, we call get_ready_tasks loop until stable, or rely on next tick.
    # In this test, we might get T-1.1/T-1.2 in this call if they appear after T-1 in iteration.
    # If not, we call get_ready_tasks() again.
    
    # Let's handle the potential need for a second call by checking state
    if not ready:
        ready = manager.get_ready_tasks()
    
    # Now T-1 should be RUNNING
    assert manager.task_states["T-1"] == TaskStatus.RUNNING
    
    ids = [t.id for t in ready]
    assert "T-1.1" in ids
    assert "T-1.2" in ids
    assert "T-2" not in ids
    
    # 2. Complete T-1.1
    manager.mark_completed("T-1.1", "Done")
    assert manager.task_states["T-1"] == TaskStatus.RUNNING # Still running
    
    # 3. Complete T-1.2
    manager.mark_completed("T-1.2", "Done")
    
    # T-1 should now be auto-completed
    assert manager.task_states["T-1"] == TaskStatus.COMPLETED
    
    # 4. Check on T-2
    # T-2 should now be ready
    ready_2 = manager.get_ready_tasks()
    ids_2 = [t.id for t in ready_2]
    assert "T-2" in ids_2
