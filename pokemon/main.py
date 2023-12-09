from fastapi import FastAPI, status, HTTPException
from sqlalchemy.ext.asyncio import async_sessionmaker
from .crud import CRUD
from .database import engine
from .schemas import showPokemon, TypePokemon, singlePokemon, Type, UserModel, Login
from typing import List
from .models import Pokemon, PokemonType, User
from sqlalchemy import select
import requests
from .hashing import Hash

app = FastAPI(
    title="Pokemon",
    description="Go and summon your favourite pokemon.",
    docs_url="/"
)

session = async_sessionmaker(
    bind= engine,
    expire_on_commit=False
)
db = CRUD()

@app.get('/pokemon', response_model= List[showPokemon], tags=['Pokemon'])
async def get_all_pokemons():
    pokemons = await db.get_all(session)

    return pokemons

@app.get('/pokemon/{pokemon_name}', response_model=singlePokemon, tags=['Pokemon'])
async def get_pokemon_by_name(pokemon_name: str):
    pokemon = await db.get_one_pokemon(session, pokemon_name)
    if pokemon:
        return pokemon
        
    raise HTTPException(status_code=404, detail=f"Pokemon {pokemon_name} is not found")

@app.get('/pokemon/{pokemon_name}/type/{pokemon_type}', response_model=List[showPokemon], tags=['Pokemon'])
async def get_pokemon_by_name_n_type(pokemon_name: str, pokemon_type: str):
    pokemon = await db.get_pokemon_name_type(session, pokemon_name, pokemon_type)
    
    if pokemon:
        return pokemon
        
    raise HTTPException(status_code=404, detail=f"Pokemon {pokemon_name} and Type {pokemon_type} not found")

@app.post('/pokemon', status_code=status.HTTP_201_CREATED, tags=['Pokemon'])
async def create_pokemon():
    api_url = "https://pokeapi.co/api/v2/pokemon/"
    for i in range(1,6):
        response = requests.get(api_url + str(i))
        if response.status_code == 200:
            jsonData = response.json()
            res_existing_pokemon = await db.is_in(session, jsonData['id'])
        
            if res_existing_pokemon is None:
                new_pokemon = Pokemon(
                    name = jsonData['name'],
                    pokemon_number = jsonData['id']
                )    
                pokemon = await db.add_pokemon(session, new_pokemon)
                if pokemon.pokemon_number:
                    dict_pokemon_type = jsonData['types']
                    for type in dict_pokemon_type:    
                        new_pokemon_type = PokemonType(
                            pokemon_id = int(pokemon.pokemon_number),
                            type = type['type']['name']
                    )  
                        pokemon_type = await db.add_pokemon_type(session, new_pokemon_type)
                
            elif res_existing_pokemon: 
                return {"message": f"Duplicate data found for ID: {jsonData['id']}"}
                    
        else:
            raise HTTPException(status_code=404, detail="Pokemon not found")     

    return {"message": "Your have summoned all pokemons"}

@app.get('/pokemon/{pokemon_no}', response_model=singlePokemon, status_code=status.HTTP_404_NOT_FOUND, tags=['Pokemon'])
async def get_pokemon_by_id(pokemon_no: int):
    pokemon = await db.get_by_id(session, pokemon_no)
    if pokemon is not None:
        return pokemon
    
    raise HTTPException(status_code=404, detail=f"Pokemon with Id {pokemon_no} is not found")

@app.get('/pokemon-types/{pokemon_no}', response_model=List[TypePokemon], tags=['Pokemon'])
async def get_pokemon_type(pokemon_no: int):
    pokemon_types = await db.get_type(session, pokemon_no)
    if pokemon_types:
        return pokemon_types
    
    raise HTTPException(status_code=404, detail=f"Pokemon Type with Pokemon Id {pokemon_no} is not found")

@app.get('/pokemon-types', response_model=Type, tags=['Pokemon'])
async def get_type_one(type_id: int):
    type = await db.one_type(session, type_id)
    if type:
        return type
    
    raise HTTPException(status_code=404, detail=f"Type with  Id {type_id} is not found")

####### User #####

@app.post('/user', status_code=status.HTTP_201_CREATED, tags=['User'])
async def create_user(request: UserModel):
    new_user = User (
        name = request.name,
        email = request.email,
        password = Hash.bcrypt(request.password)
        )  
    user = await db.add_user(session, new_user)

    return user

@app.post('/login', response_model=Login, tags=['Authentication'])
async def login(request: Login):
    user = await db.user_login(session, request={"email": request.email, "password": request.password})
    return user