from sqladmin import ModelView

from app.court.models import Court
from app.event.models import Event
# from app.eventplayer.models import EventPlayer
from app.player.models import Player


class PlayerAdmin(ModelView, model=Player):
    column_list = [Player.id,
                   Player.name,
                   Player.ntrp,
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
                   Event.description]

    icon = "fa fa-calendar"


# class EventPlayerAdmin(ModelView, model=EventPlayer):
#     column_list = [EventPlayer.id,
#                    EventPlayer.player_id,
#                    EventPlayer.event_id]