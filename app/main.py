from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .database import get_sync_session, engine, Base
from .models import Pokemon

import httpx
import logging
import requests

# Configura logging
logging.basicConfig(level=logging.INFO)

# Cria as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

# Cria a aplicação FastAPI
app = FastAPI(title="Pokédex FastAPI")

# Configura arquivos estáticos (CSS, JS, imagens)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Configura a pasta de templates HTML (Jinja2)
templates = Jinja2Templates(directory="app/templates")


# URL base da API pública de Pokémon
POKEAPI_URL = "https://pokeapi.co/api/v2/pokemon"


# Rota principal (renderiza a página HTML)
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(name="index.html", context={"request": request})


@app.get("/crud", response_class=HTMLResponse)
async def crud(request: Request):
    return templates.TemplateResponse(name="crud.html", context={"request": request})


def request_pokemon_data(name: str) -> dict | None:
    """Fetch Pokémon data from the PokeAPI.

    Args:
        name (str): The name of the Pokémon to fetch.

    Returns:
        dict | None: The Pokémon data or None if not found.
    """
    response = requests.get(f"{POKEAPI_URL}/{name.lower()}")
    if response.status_code != 200:
        logging.error(f"Pokémon {name} not found in PokeAPI.")
        return None
    return response.json()


@app.get("/api/pokemon/{name}")
async def get_pokemon(name: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{POKEAPI_URL}/{name.lower()}")

        if response.status_code != 200:
            return JSONResponse(
                status_code=404, content={"error": "Pokémon não encontrado"}
            )

        data = response.json()

        pokemon = {
            "name": data["name"].capitalize(),
            "image": data["sprites"]["front_default"],
            "types": [t["type"]["name"] for t in data["types"]],
            "height": data["height"],
            "weight": data["weight"],
        }

    try:
        with get_sync_session() as session:
            existing_pokemon = (
                session.query(Pokemon).filter_by(name=pokemon["name"]).first()
            )

            if not existing_pokemon:
                new_pokemon = Pokemon(
                    name=pokemon["name"],
                    type=", ".join(pokemon["types"]),
                    height=pokemon["height"],
                    weight=pokemon["weight"],
                )
                session.add(new_pokemon)
                session.commit()

        return pokemon

    except Exception as e:
        return JSONResponse(
            status_code=500, content={"error": f"Erro ao salvar no banco: {str(e)}"}
        )


# Rota para listar vários Pokémons
@app.get("/api/pokemons")
async def list_pokemons(limit: int = 32):
    # Cria cliente HTTP assíncrono
    async with httpx.AsyncClient() as client:
        # Busca lista de Pokémons com limite
        response = await client.get(f"{POKEAPI_URL}?limit={limit}")

        # Se der erro na API
        if response.status_code != 200:
            return JSONResponse(
                status_code=500, content={"error": "Erro ao buscar Pokémons"}
            )

        # Converte resposta para JSON
        data = response.json()

        # Retorna apenas nome e URL de cada Pokémon
        return data["results"]
