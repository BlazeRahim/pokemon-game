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
    pokemon = pokemon.capitalize()
    
    data = fetch_pokemon_data()
    pokemon_names = list(data["pokemon"].keys())
    
    print(pokemon_names)

    # print(data["pokemon"]["Tauros"])

    if not data or not data["pokemon"]["Tauros"]:
        print(pokemon)
        return {"error": "Failed to fetch Pokémon data"}

    if pokemon not in data["pokemon"]:
        return {"error": f"Pokémon '{pokemon}' not found in dataset"}

    teammates = data["pokemon"][pokemon].get("teammates", {})

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

from fastapi.responses import Response
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(status_code=204)  # No Content
