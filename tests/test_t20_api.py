import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch, AsyncMock
from t20_api.main import app
from t20.core.custom_types import Plan as RuntimePlan, Task as RuntimeTask, Role as RuntimeRole, Team as RuntimeTeam

client = TestClient(app)

# Helper for async generator mock
async def mock_run_generator(*args, **kwargs):
    # Yield a dummy task and result
    task = RuntimeTask(
        id="T1", 
        description="Test Task", 
        role="TestRole", 
        agent="TestAgent", 
        deps=[]
    )
    yield task, "Test Output Result"

@pytest.fixture
def mock_system():
    with patch("t20_api.main.system") as mock:
        # Setup mocks
        mock.orchestrator = MagicMock()
        
        async def mock_start(high_level_goal, files, plan=None):
            return RuntimePlan(
                high_level_goal=high_level_goal,
                reasoning="Test reasoning",
                roles=[RuntimeRole(title="TestRole", purpose="Test Purpose")],
                tasks=[RuntimeTask(id="T1", description="Test Task", role="TestRole", agent="TestAgent", deps=[])],
                team=None
            )
        mock.start = AsyncMock(side_effect=mock_start)
        
        # Mock run to be an async generator
        mock.run = mock_run_generator
        
        yield mock

def test_start_workflow(mock_system):
    response = client.post("/start", json={"high_level_goal": "Test Goal"})
    assert response.status_code == 202
    data = response.json()
    assert "jobId" in data
    assert data["plan"]["high_level_goal"] == "Test Goal"
    assert len(data["plan"]["tasks"]) == 1
    # Verify field mapping (deps -> requires)
    assert "requires" in data["plan"]["tasks"][0]
    assert data["plan"]["tasks"][0]["requires"] == []

def test_run_workflow(mock_system):
    # 1. Start
    start_resp = client.post("/start", json={"high_level_goal": "Test Goal"})
    assert start_resp.status_code == 202
    job_id = start_resp.json()["jobId"]
    plan = start_resp.json()["plan"]
    
    # 2. Initiate Run
    # RunRequest expects 'plan'
    run_resp = client.post(f"/runs/{job_id}", json={"plan": plan})
    assert run_resp.status_code == 202
    run_data = run_resp.json()
    assert run_data["status"] == "running"
    assert "controlUrl" in run_data
    
    # 3. Check Status
    # Since TestClient executes background tasks, the run might be finished by now
    status_resp = client.get(f"/runs/{job_id}")
    assert status_resp.status_code == 200
    status_data = status_resp.json()
    
    assert status_data["status"] in ["running", "completed"]
    if status_data["status"] == "completed":
        assert len(status_data["results"]) > 0
        assert status_data["results"][0]["output"] == "Test Output Result"

def test_history(mock_system):
    # Create a job
    client.post("/start", json={"high_level_goal": "History Test"})
    
    response = client.get("/history/runs")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["highLevelGoal"] == "History Test"
