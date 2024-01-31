from fastapi import FastAPI
from app.player.router import router as player_router
from app.court.router import router as court_router
from app.event.router import router as event_router
from app.eventplayer.router import router as eventplayer_router
app = FastAPI()
app.include_router(player_router)
app.include_router(court_router)
app.include_router(event_router)
app.include_router(eventplayer_router)
