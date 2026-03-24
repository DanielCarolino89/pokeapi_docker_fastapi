from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import httpx
from .database import get_sync_session, engine, Base
from .models import Pokemon
from .base_models import PokemonOutput
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


# Rota para buscar um Pokémon específico pelo nome
@app.get("/api/pokemon/{name}", response_model=PokemonOutput)
async def get_pokemon(name: str):
    try:
        with get_sync_session() as session:
            # Verifica se o Pokémon já existe no banco de dados
            existing_pokemon = (
                session.query(Pokemon).filter_by(name=name.capitalize()).first()
            )
            logging.info(f"Pokémon encontrado no banco: {existing_pokemon}")
            if existing_pokemon:
                return PokemonOutput(
                    id=existing_pokemon.id,
                    name=existing_pokemon.name,
                    type=existing_pokemon.type,
                    height=existing_pokemon.height,
                    weight=existing_pokemon.weight,
                )

            data = request_pokemon_data(name)
            if not data:
                return JSONResponse(
                    status_code=404, content={"error": "Pokémon not found"}
                )

            # Insert do pokemon no banco
            pokemon = Pokemon()
            pokemon.name = data["name"].capitalize()
            pokemon.type = data["types"][0]["type"]["name"]
            pokemon.height = data["height"]
            pokemon.weight = data["weight"]

            session.add(pokemon)
            session.commit()
            session.refresh(pokemon)

            return PokemonOutput(
                id=pokemon.id,
                name=pokemon.name,
                type=pokemon.type,
                height=pokemon.height,
                weight=pokemon.weight,
            )
    except Exception as e:
        logging.error(f"Erro ao processar Pokémon {name}: {e}", exc_info=True)
        return JSONResponse(status_code=500, content={"error": "Internal Server Error"})


# Rota para listar vários Pokémons
@app.get("/api/pokemons")
async def list_pokemons(limit: int = 12):
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
