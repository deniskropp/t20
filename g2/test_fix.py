
from fastapi.testclient import TestClient
from serve_g2 import app
import sys

client = TestClient(app)

def test_start_endpoint():
    print("Testing /start endpoint...")
    try:
        # We need to simulate enough for system.start to work. 
        # Since we can't easily mock the internal system without more code, 
        # we rely on the fact that the previous failure was a Validation Error on return.
        # If it returns 202, it passed validation.
        response = client.post("/start", json={
            "high_level_goal": "test goal",
            "files": []
        })
        print(f"Response status: {response.status_code}")
        if response.status_code == 202:
             print("Success: Got 202 Accepted")
             data = response.json()
             job_id = data.get('jobId')
             print(f"Job ID: {job_id}")
             
             # Now test the stream endpoint keying off the job_id
             # We just check connection, not full stream consumption for this quick test
             with client.stream("GET", f"/runs/{job_id}/stream") as stream:
                 print(f"Stream status: {stream.status_code}")
                 if stream.status_code == 200:
                     print("Stream connection successful.")
                 else:
                     print(f"Stream connection failed: {stream.status_code}")
        else:
             print(f"Failed: {response.text}")
             sys.exit(1)
            
    except Exception as e:
        print(f"Exception: {e}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        test_start_endpoint()
        print("Test passed.")
    except Exception as e:
        print(f"Test failed: {e}")
        sys.exit(1)
