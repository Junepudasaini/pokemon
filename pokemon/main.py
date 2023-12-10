from fastapi import FastAPI
from routers import authentication, user, pokemon

app = FastAPI(
    title="Pokemon",
    description="Go and summon your favourite pokemon.",
    docs_url="/"
)

app.include_router(authentication.router)
app.include_router(user.router)
app.include_router(pokemon.router)

