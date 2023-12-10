from database import Base, engine
import asyncio

async def create_db():
    async with engine.begin() as connection:
        from models import Pokemon
        from models import PokemonType
        from models import User
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)

    
    await engine.dispose()

asyncio.run(create_db())