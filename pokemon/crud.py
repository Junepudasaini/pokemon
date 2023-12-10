from fastapi import status, HTTPException
from models import Pokemon, PokemonType, User
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy import select, or_
from sqlalchemy.orm import selectinload
from hashing import Hash
import jwt

class CRUD:
    async def get_all(self, async_session: async_sessionmaker[AsyncSession]):
        async with async_session() as session:
            statement = select(Pokemon).options(selectinload(Pokemon.poke_types)).order_by(Pokemon.pokemon_number) # selectinload to eagerly load the relationships

            result = await session.execute(statement)
            pokemons =  result.scalars().all()

        # Reattach instances before we return
        for pokemon in pokemons:
            session.add(pokemon)

        return pokemons
        
    async def add_pokemon(self, async_session: async_sessionmaker[AsyncSession], pokemon: Pokemon):
        async with async_session() as session:
            session.add(pokemon)
            await session.commit()
            return pokemon
        
    async def add_pokemon_type(self, async_session: async_sessionmaker[AsyncSession], pokemon_type: PokemonType):
        async with async_session() as session:
            session.add(pokemon_type)
            await session.commit()

            return pokemon_type

    async def is_in(self, async_session: async_sessionmaker[AsyncSession], pokemon_no: int):
        async with async_session() as session:
            statement = select(Pokemon).where(Pokemon.pokemon_number == pokemon_no)
            existing_pokemon = await session.execute(statement)
            existing_pokemon = existing_pokemon.scalar_one_or_none()
            
            return existing_pokemon
            
    async def get_by_id(self, async_session: async_sessionmaker[AsyncSession], pokemon_no: int):
        async with async_session() as session:
            statement = select(Pokemon).filter(Pokemon.pokemon_number == pokemon_no)
            result = await session.execute(statement)
            pokemon = result.scalar_one_or_none()
                
            return pokemon
        
    async def get_one_pokemon(self, async_session: async_sessionmaker[AsyncSession], pokemon_name: str):
        async with async_session() as session:
            statement = select(Pokemon).filter(Pokemon.name == pokemon_name)
            result = await session.execute(statement)
            pokemon = result.scalar_one_or_none()
            return pokemon
        
    async def get_pokemon_name_type(self, async_session:async_sessionmaker[AsyncSession], pokemon_name: str, pokemon_type: str):
        async with async_session() as session:
            statement = select(Pokemon).options(selectinload(Pokemon.poke_types)).join(Pokemon.poke_types).where(or_(PokemonType.type == pokemon_type, Pokemon.name == pokemon_name))
            result = await session.execute(statement)
            result =  result.scalars().all()
            for row in result:
                session.add(row)
            return result
        
    async def get_type(self, async_session: async_sessionmaker[AsyncSession], pokemon_no: int):
        async with async_session() as session:
            statement = select(PokemonType).filter(PokemonType.pokemon_id == pokemon_no)

            result = await session.execute(statement)
            pokemon = result.scalars().all()
            return pokemon   
        
    async def one_type(self, async_session: async_sessionmaker[AsyncSession], type_id: int):
        async with async_session() as session:
            statement = select(PokemonType).filter(PokemonType.id == type_id)

            result = await session.execute(statement)
            type = result.scalar_one_or_none()
            return type
 
    async def add_user(self, async_session: async_sessionmaker[AsyncSession], user: User):
        async with async_session() as session:
            statement = select(User).filter(User.email == user.email)
            result = await session.execute(statement)
            existing_user_in_db = result.scalar_one_or_none()
            
            if existing_user_in_db is not None:
                raise HTTPException(status_code=403, detail=f"Email {user.email} already exists.")
            
            session.add(user)
            await session.commit()
            return user
        
    async def user_login(self, async_session: async_sessionmaker[AsyncSession], request):
        async with async_session() as session:
            statement = select(User).filter(User.email == request.username)
            result = await session.execute(statement)

            user_from_db  = result.scalar_one_or_none()
           
            if user_from_db is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with the email {request.username} do not match.")
            else:
                res_verify = await Hash.verify(user_from_db.password, request.password)
                if not res_verify:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")
                
                access_token = await jwt.create_access_token(data={"sub": user_from_db.email})
                return {"access_token": access_token, "token_type": "bearer"}
            