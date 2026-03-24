from uuid import UUID, uuid4

from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class Pokemon(Base):
    __tablename__ = "pokemons"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default_factory=uuid4,
        init=False,
        doc="Primary key: unique identifier.",
    )
    name: Mapped[str | None] = mapped_column(
        String(255),
        default=None,
        nullable=True,
        doc="Name of the Pokémon.",
    )
    type: Mapped[str | None] = mapped_column(
        String(50),
        default=None,
        nullable=True,
        doc="Type of the Pokémon (e.g., Fire, Water, Grass).",
    )

    height: Mapped[int | None] = mapped_column(
        default=None,
        nullable=True,
        doc="Height of the Pokémon in meters.",
    )

    weight: Mapped[int | None] = mapped_column(
        default=None,
        nullable=True,
        doc="Weight of the Pokémon in kilograms.",
    )
