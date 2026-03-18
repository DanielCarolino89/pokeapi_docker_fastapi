from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import httpx

app = FastAPI(title="Pokédex FastAPI")

# Arquivos estáticos (CSS/JS)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Templates HTML
templates = Jinja2Templates(directory="app/templates")

POKEAPI_URL = "https://pokeapi.co/api/v2/pokemon"

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/pokemon/{name}")
async def get_pokemon(name: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{POKEAPI_URL}/{name.lower()}")

        if response.status_code != 200:
            return JSONResponse(
                status_code=404,
                content={"error": "Pokémon não encontrado"}
            )

        data = response.json()

        pokemon = {
            "name": data["name"].capitalize(),
            "image": data["sprites"]["front_default"],
            "types": [t["type"]["name"] for t in data["types"]],
            "height": data["height"],
            "weight": data["weight"]
        }

        return pokemon

@app.get("/api/pokemons")
async def list_pokemons(limit: int = 12):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{POKEAPI_URL}?limit={limit}")

        if response.status_code != 200:
            return JSONResponse(
                status_code=500,
                content={"error": "Erro ao buscar Pokémons"}
            )

        data = response.json()
        return data["results"]
