from models.player import Player
from models import db
from datetime import datetime
from .base import BaseService, ServiceResponse


class PlayerService(BaseService):
    def get_player_by_id(self, player_id):
        player = Player.query.get(player_id)
        if player:
            return ServiceResponse(True, data=player)
        return ServiceResponse(False, message="Player not found.")

    def update_player_activity(self, player_id):
        player = Player.query.get(player_id)
        if player:
            player.last_activity_date = datetime.utcnow()
            player.online = True
            self.db.session.commit()
            return ServiceResponse(True, data=player)
        return ServiceResponse(False, message="Player not found.")

    def set_player_offline(self, player_id):
        player = Player.query.get(player_id)
        if player:
            player.online = False
            self.db.session.commit()
            return ServiceResponse(True, data=player)
        return ServiceResponse(False, message="Player not found.")

    def update_player_currency(self, player_id, fishbucks=None, fishcoins=None):
        player = Player.query.get(player_id)
        if player:
            if fishbucks is not None:
                player.fishbucks = fishbucks
            if fishcoins is not None:
                player.fishcoins = fishcoins
            self.db.session.commit()
            return ServiceResponse(True, data=player)
        return ServiceResponse(False, message="Player not found.")

    def add_experience(self, player_id, xp_amount):
        player = Player.query.get(player_id)
        if player:
            player.xp += xp_amount
            new_level = (player.xp // 1000) + 1
            if new_level > player.level:
                player.level = new_level
            self.db.session.commit()
            return ServiceResponse(True, data=player)
        return ServiceResponse(False, message="Player not found.")

    def get_player_stats(self, player_id):
        player = Player.query.get(player_id)
        if player:
            stats = {
                'id': player.id,
                'username': player.username,
                'level': player.level,
                'xp': player.xp,
                'fishbucks': player.fishbucks,
                'fishcoins': player.fishcoins,
                'energy': player.energy,
                'online': player.online,
                'last_activity': player.last_activity_date,
                'created_date': player.created_date,
                'last_login': player.last_login
            }
            return ServiceResponse(True, data=stats)
        return ServiceResponse(False, message="Player not found.")
