from cgi import print_form
from fastapi import FastAPI, Query
import requests

app = FastAPI()

SMOGON_API_URL = "https://pkmn.github.io/smogon/data/stats/gen1ou.json"

def fetch_pokemon_data():
    """Fetch Pokémon data from Smogon API."""
    response = requests.get(SMOGON_API_URL)
    if response.status_code == 200:
        # print(response.json())
        return response.json()
    return None

def find_best_teammates(pokemon: str, limit: int = 5):
    """Find optimal teammates for a given Pokémon dynamically."""
    pokemon = pokemon.lower()
    
    data = fetch_pokemon_data()
    print(data)
    if not data or pokemon not in data:
        return {"error": "Failed to fetch Pokémon data"}

    if pokemon not in data["pokemon"][pokemon]:
        return {"error": f"Pokémon '{pokemon}' not found in dataset"}

    teammates = data["data"][pokemon].get("teammates", {})

    # Sort teammates by usage percentage
    sorted_teammates = sorted(teammates.items(), key=lambda x: x[1], reverse=True)
    
    return {
        "pokemon": pokemon,
        "recommended_teammates": [{"name": name, "usage": usage} for name, usage in sorted_teammates[:limit]]
    }

@app.get("/suggest_teammates/")
async def suggest_teammates(pokemon: str = Query(..., description="Enter Pokémon name"), limit: int = 5):
    """API endpoint to suggest Pokémon teammates."""
    return find_best_teammates(pokemon, limit)
