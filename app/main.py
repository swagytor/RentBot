from fastapi import FastAPI
from sqladmin import Admin

from app.admin.admin import CourtAdmin, PlayerAdmin, EventAdmin
from app.database import engine

from app.player.router import router as player_router
from app.court.router import router as court_router
from app.event.router import router as event_router
# from app.eventplayer.router import router as eventplayer_router

app = FastAPI(swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"})
admin = Admin(app, engine)

admin.add_view(CourtAdmin)
admin.add_view(PlayerAdmin)
admin.add_view(EventAdmin)
# admin.add_view(EventPlayerAdmin)

app.include_router(player_router)
app.include_router(court_router)
app.include_router(event_router)
# app.include_router(eventplayer_router)


