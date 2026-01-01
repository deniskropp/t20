import asyncio
import logging
from t20sdk.core.ntfy import NtfyClient

# Setup basic logging to see the output
logging.basicConfig(level=logging.INFO)

async def main():
    topic = "t20_manual_test"
    print(f"=== Ntfy Verification Script ===")
    print(f"Using topic: {topic}")
    
    client = NtfyClient(topic=topic)
    
    print("Sending confirmation request...")
    print(f"Please go to https://ntfy.violass.club/{topic} and click 'Yes' or 'No'.")
    
    # This should block until we click a button
    result = await client.send_confirmation_request("This is a test request. Please click a button.")
    
    if result:
        print("\nSUCCESS: Received APPROVED response!")
    else:
        print("\nSUCCESS: Received REJECTED response!")

if __name__ == "__main__":
    asyncio.run(main())
