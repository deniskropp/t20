import asyncio
import httpx
import sys

BASE_URL = "http://localhost:8000"

async def test_prompts_crud():
    print(f"Connecting to {BASE_URL}...")
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=10.0) as client:
        # Create
        print("Creating prompt...")
        response = await client.post("/prompts/", json={
            "name": "Test Prompt",
            "type": "system",
            "content": "You are a test agent."
        })
        if response.status_code != 201:
            print(f"Failed to create prompt: {response.text}")
            sys.exit(1)
        prompt = response.json()
        print(f"Created prompt: {prompt}")
        prompt_id = prompt["id"]

        # List
        print("Listing prompts...")
        response = await client.get("/prompts/")
        assert response.status_code == 200
        prompts = response.json()
        print(f"Found {len(prompts)} prompts")
        assert any(p["id"] == prompt_id for p in prompts)

        # Get
        print(f"Getting prompt {prompt_id}...")
        response = await client.get(f"/prompts/{prompt_id}")
        assert response.status_code == 200
        assert response.json()["content"] == "You are a test agent."

        # Update
        print(f"Updating prompt {prompt_id}...")
        response = await client.put(f"/prompts/{prompt_id}", json={
            "content": "You are an updated test agent."
        })
        assert response.status_code == 200
        assert response.json()["content"] == "You are an updated test agent."

        # Delete
        print(f"Deleting prompt {prompt_id}...")
        response = await client.delete(f"/prompts/{prompt_id}")
        assert response.status_code == 204

        # Verify Delete
        print(f"Verifying deletion...")
        response = await client.get(f"/prompts/{prompt_id}")
        assert response.status_code == 404
        print("Verified deletion (404).")

        print("\nAll Prompt API tests passed!")

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(test_prompts_crud())
    except Exception as e:
        print(f"Test failed with exception: {e}")
        sys.exit(1)
