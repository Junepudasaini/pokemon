from database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from datetime import datetime
from typing import List


class Pokemon(Base):
    __tablename__ = 'pokemons'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False)
    pokemon_number: Mapped[int] = mapped_column(unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    poke_types: Mapped[List["PokemonType"]] = relationship(back_populates='pokemons')

    def __repr__(self) -> str:
        return f"<Pokemon {self.name} at {self.created_at}>"
    
    
class PokemonType(Base):
    __tablename__ = 'pokemon_types'
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    pokemon_id: Mapped[int] = mapped_column(ForeignKey("pokemons.pokemon_number"))
    type: Mapped[str] = mapped_column(nullable=False)

    pokemons: Mapped["Pokemon"] = relationship(back_populates='poke_types')
    
    def __repr__(self) -> str:
        return f"<Pokemon {self.pokemons.name}  is type of {self.type}>"
    
class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<User {self.name} created at {self.created_at}>"