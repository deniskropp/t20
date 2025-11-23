import json
from typing import List, Dict, Any

class Orchestrator:
    def __init__(self, director_agent, scriptwriter_agent):
        self.director_agent = director_agent
        self.scriptwriter_agent = scriptwriter_agent

    def run_film_production(self, topic: str, character_limit: int, locations: List[str],
                            optional_positions: List[str], all_actions: List[Dict[str, str]],
                            all_shots: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Orchestrates the film production process from character profiling to script generation.

        Args:
            topic (str): The central theme or topic of the film.
            character_limit (int): The maximum number of characters allowed.
            locations (List[str]): A list of available locations for scenes.
            optional_positions (List[str]): A list of optional positions for characters in scenes.
            all_actions (List[Dict[str, str]]): A list of all available actions for characters.
            all_shots (List[Dict[str, str]]): A list of all available shots.

        Returns:
            Dict[str, Any]: A dictionary containing the complete film script and character profiles.
        """
        print("Orchestrator: Starting film production process...")

        # Step 1: Director Agent - Brainstorm and define core elements
        print("Orchestrator: Delegating to Director Agent for character profiling and high-level script planning.")
        director_output_json = self.director_agent.generate_film_elements(topic, character_limit, locations)
        director_output = json.loads(director_output_json)

        character_profiles = director_output["character_profiles"]
        high_level_scene_info = director_output["scene_information"]

        print("Orchestrator: Director Agent completed. Character Profiles and High-Level Scene Info received.")
        # print(f"Character Profiles: {json.dumps(character_profiles, indent=2)}")
        # print(f"High-Level Scene Info: {json.dumps(high_level_scene_info, indent=2)}")

        # Prepare data for ScriptWriter
        male_characters = [p["name"] for p in character_profiles if p["gender"].lower() == "male"]
        female_characters = [p["name"] for p in character_profiles if p["gender"].lower() == "female"]

        # Step 2-6: ScriptWriter Agent - Generate the full script
        print("Orchestrator: Delegating to ScriptWriter Agent for detailed script generation.")
        scriptwriter_output_json = self.scriptwriter_agent.write_script(
            character_profiles,
            high_level_scene_info,
            male_characters,
            female_characters,
            locations,
            optional_positions,
            all_actions,
            all_shots
        )
        full_script = json.loads(scriptwriter_output_json)

        print("Orchestrator: ScriptWriter Agent completed. Full script received.")
        # print(f"Full Script: {json.dumps(full_script, indent=2)}")

        return {
            "character_profiles": character_profiles,
            "script": full_script
        }

class DirectorAgent:
    def __init__(self, llm):
        self.llm = llm
        self.instructions_path = "/home/einrichten/t20/prompts/filmagent director_instructions.txt"
        self.output_format_path = "/home/einrichten/t20/prompts/filmagent director_instructions.txt" # The output format is embedded in the instructions

    def generate_film_elements(self, topic: str, character_limit: int, locations: List[str]) -> str:
        with open(self.instructions_path, 'r') as f:
            instructions = f.read()

        prompt = f"""{instructions}

The film's topic is: "{topic}"
Character limit: {character_limit}
Available locations: {', '.join(locations)}

Please generate the character profiles and high-level scene information according to the specified output format.
"""
        print("DirectorAgent: Generating film elements...")
        response = self.llm.generate_response(prompt)
        print("DirectorAgent: Film elements generated.")
        return response

class ScriptWriterAgent:
    def __init__(self, llm):
        self.llm = llm
        self.instructions_path = "/home/einrichten/t20/prompts/filmagent scriptwriter_instructions.txt"
        self.output_format_path = "/home/einrichten/t20/prompts/filmagent scriptwriter_instructions.txt" # The output format is embedded in the instructions

    def write_script(self, character_profiles: List[Dict[str, Any]],
                     high_level_scene_info: List[Dict[str, Any]],
                     male_characters: List[str], female_characters: List[str],
                     locations: List[str], optional_positions: List[str],
                     all_actions: List[Dict[str, str]], all_shots: List[Dict[str, str]]) -> str:

        with open(self.instructions_path, 'r') as f:
            instructions = f.read()

        # Format character profiles for the prompt
        profiles_str = json.dumps(character_profiles, indent=2)
        # Prepare high-level scene info for the prompt (especially for Step 1)
        # The scriptwriter instructions expect a list of scene_information dictionaries
        # with 'who', 'where', 'what' keys. The director already provides this.
        scene_info_for_scriptwriter = json.dumps(high_level_scene_info, indent=2)

        # Prepare locations string for the prompt
        locations_str = "\n".join([f"{i+1}. {loc}" for i, loc in enumerate(locations)])

        # Prepare optional positions string for the prompt
        optional_positions_str = "\n".join(optional_positions)

        # Prepare all actions string for the prompt
        all_actions_str = json.dumps(all_actions, indent=2)

        # Prepare all shots string for the prompt
        all_shots_str = json.dumps(all_shots, indent=2)

        prompt = f"""{instructions}

#### Characters' Profile:
{profiles_str}

#### Main Characters:
1. **Male**: {', '.join(male_characters)}
2. **Female**: {', '.join(female_characters)}

#### Main Locations:
{locations_str}

#### Optional Positions:
{optional_positions_str}

#### [Complete List of Actions]:
{all_actions_str}

#### [Complete List of Shots]:
{all_shots_str}

Here is the high-level scene information from the Director Agent, which you should use as a basis for your detailed script generation, especially for Step 1:
{scene_info_for_scriptwriter}

Please generate the complete film script by strictly following the 5-step process outlined in your instructions.
"""
        print("ScriptWriterAgent: Writing script...")
        response = self.llm.generate_response(prompt)
        print("ScriptWriterAgent: Script written.")
        return response

class LLM:
    def __init__(self, model_name: str = "gpt-4o"):
        from openai import OpenAI
        self.client = OpenAI()
        self.model_name = model_name

    def generate_response(self, prompt: str, temperature: float = 0.7, max_tokens: int = 4000) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are a helpful AI assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error generating response from LLM: {e}")
            return json.dumps({"error": str(e)})


if __name__ == "__main__":
    # Initialize LLM
    llm_model = LLM()

    # Initialize Agents
    director = DirectorAgent(llm_model)
    scriptwriter = ScriptWriterAgent(llm_model)
    orchestrator = Orchestrator(director, scriptwriter)

    # Define film parameters
    film_topic = "A detective's last case before retirement, uncovering a conspiracy."
    char_limit = 4
    available_locations = [
        "Apartment living room", "Apartment kitchen", "Roadside", "Gaming room",
        "Meeting room", "Storehouse", "Relaxing Room", "Reception Room",
        "Sofa Corner", "Large kitchen", "Beverage Room", "Office",
        "Dining Room", "Billiard room", "Work room"
    ]
    optional_positions_list = [
        "Position A", "Position B", "Position C", "Position D", "Position E",
        "Position F", "Position G", "Position H", "Position I", "Position J"
    ]
    all_actions_list = [
        {"action": "Walk", "state": "standing"},
        {"action": "Run", "state": "standing"},
        {"action": "Sit Down", "state": "standing"},
        {"action": "Stand Up", "state": "sitting"},
        {"action": "Talk", "state": "standing"},
        {"action": "Talk", "state": "sitting"},
        {"action": "Listen", "state": "standing"},
        {"action": "Listen", "state": "sitting"},
        {"action": "Look Around", "state": "standing"},
        {"action": "Look Around", "state": "sitting"},
        {"action": "Drink", "state": "standing"},
        {"action": "Drink", "state": "sitting"},
        {"action": "Eat", "state": "sitting"},
        {"action": "Nod", "state": "standing"},
        {"action": "Nod", "state": "sitting"},
        {"action": "Shake Head", "state": "standing"},
        {"action": "Shake Head", "state": "sitting"},
        {"action": "Point", "state": "standing"},
        {"action": "Point", "state": "sitting"},
        {"action": "Laugh", "state": "standing"},
        {"action": "Laugh", "state": "sitting"},
        {"action": "Sigh", "state": "standing"},
        {"action": "Sigh", "state": "sitting"},
        {"action": "Read", "state": "sitting"},
        {"action": "Write", "state": "sitting"},
        {"action": "Type", "state": "sitting"},
        {"action": "Lean Back", "state": "sitting"},
        {"action": "Cross Arms", "state": "standing"},
        {"action": "Cross Arms", "state": "sitting"},
        {"action": "Pace", "state": "standing"},
        {"action": "Frown", "state": "standing"},
        {"action": "Frown", "state": "sitting"},
        {"action": "Smile", "state": "standing"},
        {"action": "Smile", "state": "sitting"},
        {"action": "Gesture", "state": "standing"},
        {"action": "Gesture", "state": "sitting"},
        {"action": "Shrug", "state": "standing"},
        {"action": "Shrug", "state": "sitting"}
    ]
    all_shots_list = [
        {"shot_type": "Long Shot", "usage_conditions": "Establishes scene, shows full body of characters, good for dialogue-starting scenes."},
        {"shot_type": "Mid Shot", "usage_conditions": "Shows characters from waist up, good for showing interaction between characters."},
        {"shot_type": "Close Up", "usage_conditions": "Focuses on character's face or specific object, emphasizes emotion or detail."},
        {"shot_type": "Track Shot", "usage_conditions": "Follows a character or object in motion, good for dialogue-starting scenes."},
        {"shot_type": "Pan Shot", "usage_conditions": "Camera pivots horizontally, reveals surroundings or follows action, can be used multiple times in a row during dialogue."},
        {"shot_type": "Zoom Shot", "usage_conditions": "Changes focal length to magnify or de-magnify, must be preceded by a Long Shot."}
    ]

    # Run the orchestration
    final_output = orchestrator.run_film_production(
        film_topic,
        char_limit,
        available_locations,
        optional_positions_list,
        all_actions_list,
        all_shots_list
    )

    # Print the final output
    print("\n--- Final Film Production Output ---")
    print(json.dumps(final_output, indent=2))
