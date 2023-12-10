from fastapi import APIRouter, status, Depends, HTTPException
from typing import List
from crud import CRUD
from models import Pokemon, PokemonType
from schemas import UserModel, singlePokemon, showPokemon, TypePokemon
from database import session
import requests
import oauth2

router = APIRouter(
    tags=['Pokemon']
)

db = CRUD()
 
# Fetch all Pokemons to database

@router.post('/pokemon', status_code=status.HTTP_201_CREATED)
async def create_pokemon(current_user: UserModel = Depends(oauth2.get_current_user)):
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

# Get all Pokemons

@router.get('/pokemon', response_model= List[showPokemon])
async def get_all_pokemons(current_user: UserModel = Depends(oauth2.get_current_user)):
    pokemons = await db.get_all(session)

    return pokemons

# Get Pokemon by it's name

@router.get('/pokemon/name/{pokemon_name}', response_model=singlePokemon) 
async def get_pokemon_by_name(pokemon_name: str, current_user: UserModel = Depends(oauth2.get_current_user)):
    pokemon = await db.get_one_pokemon(session, pokemon_name)
    if pokemon:
        return pokemon
        
    raise HTTPException(status_code=404, detail=f"Pokemon {pokemon_name} is not found")

# Get Pokemon by it's name and types

@router.get('/pokemon/{pokemon_name}/type/{pokemon_type}', response_model=List[showPokemon])
async def get_pokemon_by_name_n_type(pokemon_name: str, pokemon_type: str, current_user: UserModel = Depends(oauth2.get_current_user)):
    pokemon = await db.get_pokemon_name_type(session, pokemon_name, pokemon_type)
    
    if pokemon:
        return pokemon
        
    raise HTTPException(status_code=404, detail=f"Pokemon {pokemon_name} and Type {pokemon_type} not found")

# Get Pokemon by it's number

@router.get('/pokemon/{pokemon_no}', response_model=singlePokemon)
async def get_pokemon_by_id(pokemon_no: int, current_user: UserModel = Depends(oauth2.get_current_user)):
    pokemon = await db.get_by_id(session, pokemon_no)
    
    if pokemon is not None:
        return pokemon
    
    raise HTTPException(status_code=404, detail=f"Pokemon with Id {pokemon_no} is not found")

# Get Pokemon's type by it's number

@router.get('/pokemon/types/{pokemon_no}', response_model=List[TypePokemon])
async def get_pokemon_type(pokemon_no: int, current_user: UserModel = Depends(oauth2.get_current_user)):
    pokemon_types = await db.get_type(session, pokemon_no)
    if pokemon_types:
        return pokemon_types
    
    raise HTTPException(status_code=404, detail=f"Pokemon Type with Pokemon Id {pokemon_no} is not found")