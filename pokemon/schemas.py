from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List


class Type(BaseModel):
    type: str
    pokemon_id: int
    model_config = ConfigDict(
        from_attributes= True
    )

class singlePokemon(BaseModel):
    pokemon_number: int
    name: str
    created_at: datetime
    model_config = ConfigDict(
        from_attributes= True
    )

class showPokemon(BaseModel):
    pokemon_number: int
    name: str
    poke_types: List[Type]
    created_at: datetime

    model_config = ConfigDict(
        from_attributes= True
    )

class TypePokemon(BaseModel):
    pokemon_id: int
    type: str
    # pokemons: showPokemon
    model_config = ConfigDict(
        from_attributes= True
    )

class PokemonCreateModel(BaseModel):
    name: str

    model_config = ConfigDict(
        from_attributes= True,
        json_schema_extra={
            'name':'Pokemon'
        }
    )

class UserModel(BaseModel):
    name: str
    email: str
    password: str

class Login(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None

