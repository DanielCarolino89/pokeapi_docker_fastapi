from pydantic import BaseModel
from uuid import UUID


class PokemonOutput(BaseModel):
    id: UUID | str | None = None
    name: str | None = None
    type: str | None = None
    height: int | None = None
    weight: int | None = None
