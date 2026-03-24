from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import httpx

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


# Rota para buscar um Pokémon específico pelo nome
@app.get("/api/pokemon/{name}")
async def get_pokemon(name: str):
    # Cria cliente HTTP assíncrono
    async with httpx.AsyncClient() as client:
        # Faz requisição para a PokeAPI
        response = await client.get(f"{POKEAPI_URL}/{name.lower()}")

        # Se não encontrar, retorna erro 404
        if response.status_code != 200:
            return JSONResponse(
                status_code=404, content={"error": "Pokémon não encontrado"}
            )

        # Converte resposta para JSON
        data = response.json()

        # Monta um objeto simplificado
        pokemon = {
            "name": data["name"].capitalize(),  # Nome com primeira letra maiúscula
            "image": data["sprites"]["front_default"],  # Imagem padrão
            "types": [t["type"]["name"] for t in data["types"]],  # Lista de tipos
            "height": data["height"],  # Altura
            "weight": data["weight"],  # Peso
        }

        return pokemon  # Retorna JSON com os dados do Pokémon


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
