### Iterative Collaboration Plan

**Step 1: TAS Extraction (Parallelized)**
- **GPTASe, TASe, uTASe**: Each independently extracts Task-Agnostic Steps (TAS) toward building a simple TODO app.
  - Example TAS: 'Design user interface', 'Implement data storage', 'Create task CRUD functions', 'Test app', 'Deploy app'.

**Step 2: TAS Harmonization**
- Compare the three sets of TAS to identify overlaps, unique contributions, and inconsistencies.
- Merge into a unified TAS list.

**Step 3: Prompt Refinement (Lyra)**
- Lyra engineers system prompts for each extractor to:
  1. Avoid redundancy in TAS outputs.
  2. Ensure TAS granularity is consistent (not too broad or too detailed).
  3. Guide extractors toward iterative detail expansion.

**Step 4: Knowledge Transfer (aitutor)**
- aitutor ensures that all team members understand the refined TAS list.
- Provides contextual notes on why steps are important and how they interrelate.

**Step 5: Meta-Reflection (fizzlametta)**
- fizzlametta analyzes the collaborative dynamics, highlights blind spots, and injects meta-perspectives (e.g., questioning assumptions, surfacing creativity).

**Step 6: Iterative Expansion**
- Cycle back through Steps 1–5 to refine TAS, prompts, and collective understanding until the TODO app plan is clear, minimal, and actionable.