from sqladmin import ModelView

from app.court.models import Court
from app.event.models import Event
from app.player.models import Player


class PlayerAdmin(ModelView, model=Player):
    column_list = [Player.id,
                   Player.name,
                   Player.NTRP,
                   Player.tg_id,
                   Player.tg_username,
                   Player.games_played_on_week,
                   Player.is_notification,
                   Player.is_notification_changes]

    icon = "fa fa-user"


class CourtAdmin(ModelView, model=Court):
    column_list = [Court.id,
                   Court.name,
                   Court.address]

    icon = "fa fa-map-marker"


class EventAdmin(ModelView, model=Event):
    column_list = [Event.id,
                   Event.start_time,
                   Event.finish_time,
                   Event.court,
                   Event.players,
                   Event.description]

    icon = "fa fa-calendar"
