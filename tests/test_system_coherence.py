import pytest
import asyncio
from runtime.system import System
from runtime.task_manager import TaskManager, TaskStatus
from runtime.custom_types import Plan, Task, Role
from runtime.message_bus import SpaceMessage

@pytest.mark.asyncio
async def test_agent_loading():
    system = System(root_dir="/home/einrichten/t20")
    system.setup(orchestrator_name="LiLo")
    assert system.orchestrator is not None
    assert system.orchestrator.profile.name == "LiLo"
    assert len(system.agents) > 0

@pytest.mark.asyncio
async def test_task_manager():
    plan = Plan(
        high_level_goal="Test Goal",
        reasoning="Test Reasoning",
        roles=[Role(title="Tester", purpose="Testing")],
        tasks=[
            Task(id="1", description="Task 1", role="Tester", agent="LiLo", deps=[]),
            Task(id="2", description="Task 2", role="Tester", agent="LiLo", deps=["1"])
        ]
    )
    tm = TaskManager(plan)
    
    ready = tm.get_ready_tasks()
    assert len(ready) == 1
    assert ready[0].id == "1"
    
    tm.mark_completed("1", "Result 1")
    
    ready = tm.get_ready_tasks()
    assert len(ready) == 1
    assert ready[0].id == "2"

@pytest.mark.asyncio
async def test_message_bus():
    from runtime.message_bus import MessageBus
    bus = MessageBus()
    received = []
    
    def callback(msg):
        received.append(msg)
        
    bus.subscribe("test_topic", callback)
    
    msg = "⫻test/meta:log/1\nHello"
    bus.publish("test_topic", msg)
    
    assert len(received) == 1
    assert "Hello" in received[0]

if __name__ == "__main__":
    asyncio.run(test_agent_loading())
    asyncio.run(test_task_manager())
    asyncio.run(test_message_bus())
