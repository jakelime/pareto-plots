import itertools
import random
from typing import List


def generate_toy_story_machine_names(count: int = 100) -> List[str]:
    """
    Generates a list of unique machine names inspired by characters, objects,
    and themes from the Toy Story franchise.

    The function uses cartesian product to ensure a large pool of unique
    combinations, which are then shuffled and sliced to return the exact
    number requested. The current pool size is 63 prefixes * 63 suffixes = 3969 names.

    Args:
        count: The desired number of unique names to generate. Defaults to 100.

    Returns:
        A list of generated machine names (e.g., "Buzz-Core", "Pizza-Node").
    """

    # --- Toy Story Inspired Prefixes (Characters, Objects, Locations, Phrases) ---
    prefixes = [
        "Buzz",
        "Woody",
        "Jessie",
        "Rex",
        "Hamm",
        "Slinky",
        "BoPeep",
        "Alien",
        "Zurg",
        "Lotso",
        "Star",
        "Pizza",
        "Claw",
        "Bullseye",
        "Andy",
        "Infini",
        "Beyond",
        "RC",
        "Tricera",
        "Bucket",
        "GreenArmy",
        # Expanded Toy Story names:
        "Dolly",
        "Trixie",
        "PotatoHead",
        "Forky",
        "Ducky",
        "Bunny",
        "Caboom",
        "Gabby",
        "Peas",
        "Wheezy",
        "Barbie",
        "Ken",
        "Etch",
        "Rocky",
        "CombatCarl",
        "Janie",
        "Sharky",
        "Chuckles",
        "Twitch",
        "Stretch",
        "Chunk",
        "Sparks",
        "RoadRunner",
        "Linguini",
        "Sid",
        "Sunnyside",
        "AlToy",
        "ToyBarn",
        "Pawn",
        "Rocket",
        "SpaceRanger",
        "Sheriff",
        "Deputy",
        "WildWest",
        "Playhouse",
        "Cloud",
        "Plasma",
        "Laser",
        "Power",
        "Friend",
        "Loyal",
        "Playtime",
        "Adventure",
        "Destiny",
        "Mission",
        "Dinoco",
        "Sky",
        "Reach",
        "Garage",
        "Attic",
        "Dumpster",
        "TriCounty",
        "Ceiling",
        "Rebel",
    ]

    # --- Machine/System Inspired Suffixes (Technology Terms) ---
    suffixes = [
        "Core",
        "Server",
        "Node",
        "Unit",
        "Engine",
        "Bot",
        "Link",
        "System",
        "Hub",
        "Module",
        "Command",
        "Bay",
        "Delta",
        "Forge",
        "Relay",
        "Matrix",
        "Guard",
        "Pilot",
        "Transit",
        "Compute",
        "Box",
        # Expanded Technical terms:
        "Cluster",
        "Cloud",
        "Stack",
        "Layer",
        "Proxy",
        "Gateway",
        "Vault",
        "Array",
        "Cache",
        "Stream",
        "Beacon",
        "Conduit",
        "Frame",
        "Host",
        "Grid",
        "Fabric",
        "Zone",
        "Cell",
        "Router",
        "Switch",
        "Worker",
        "Handler",
        "Agent",
        "Controller",
        "Manager",
        "Monitor",
        "Supervisor",
        "Director",
        "Keeper",
        "Logger",
        "Scanner",
        "Indexer",
        "Pylon",
        "Sentinel",
        "Nexus",
        "Orbit",
        "Vector",
        "Chronos",
        "Atlas",
        "Titan",
        "Nova",
        "Xfer",
        "Port",
        "Pipe",
        "Data",
        "Wire",
        "Beam",
        "Drive",
        "Logic",
        "Output",
        "Input",
        "Terminal",
    ]

    # Check if the number of prefixes/suffixes meets the expansion request
    if len(prefixes) < 60 or len(suffixes) < 60:
        # Note: This is a safety check for future modifications, current count is 63 for both.
        print(
            "Warning: Prefix or Suffix list is smaller than expected after expansion."
        )

    # Generate all possible combinations using itertools.product
    all_combinations = list(itertools.product(prefixes, suffixes))

    # Shuffle the combinations to ensure a random selection each time
    random.shuffle(all_combinations)

    # Select the first 'count' combinations
    # If the user requests more names than possible, we return all combinations
    selected_combinations = all_combinations[:count]

    # Format names as "Prefix-Suffix"
    machine_names = [f"{prefix}-{suffix}" for prefix, suffix in selected_combinations]

    return machine_names


# --- Script Execution ---
if __name__ == "__main__":
    # Generate the requested 100 names
    NUMBER_OF_NAMES = 100
    names = generate_toy_story_machine_names(count=NUMBER_OF_NAMES)

    print(f"--- Generated {len(names)} Unique Machine Names (Toy Story Theme) ---")

    # Print the list in a numbered, readable format
    for i, name in enumerate(names, 1):
        print(f"{i:03d}. {name}")
