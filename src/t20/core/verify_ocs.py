import asyncio
from t20.core.dream_to_life import DreamToLife
from t20.core.dopamine_engine import DopamineEngine

async def verify_ocs_integration():
    print("--- Verifying DreamToLife Integration ---")
    dtl = DreamToLife()
    dream_narrative = "I was flying over a city of glass, but I couldn't find a place to land."
    result = await dtl.ingest_dream_narrative(dream_narrative)
    print(f"Result: {result}")
    
    print("\n--- Verifying DopamineEngine Integration ---")
    dopamine = DopamineEngine()
    # Simulate low engagement
    print("Simulating low engagement (0.5)...")
    result_low = await dopamine.monitor_engagement(0.5)
    print(f"Result (Low): {result_low}")
    
    # Simulate high engagement
    print("Simulating high engagement (1.5)...")
    result_high = await dopamine.monitor_engagement(1.5)
    print(f"Result (High): {result_high}")

if __name__ == "__main__":
    asyncio.run(verify_ocs_integration())
