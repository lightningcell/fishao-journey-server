from models.player import Player
from models import db
from datetime import datetime
from .base import BaseService, ServiceResponse


class PlayerService(BaseService):
    def get_player_by_id(self, player_id):
        player = Player.get(player_id)
        if player:
            return ServiceResponse(True, data=player)
        return ServiceResponse(False, message="Player not found.")

    def update_player_activity(self, player_id):
        player = Player.get(player_id)
        if player:
            player.change(
                last_activity_date=datetime.utcnow(),
                online=True
            ).commit()
            return ServiceResponse(True, data=player)
        return ServiceResponse(False, message="Player not found.")

    def set_player_offline(self, player_id):
        player = Player.get(player_id)
        if player:
            player.change(online=False).commit()
            return ServiceResponse(True, data=player)
        return ServiceResponse(False, message="Player not found.")

    def update_player_currency(self, player_id, fishbucks=None, fishcoins=None):
        player = Player.get(player_id)
        if player:
            update_data = {}
            if fishbucks is not None:
                update_data['fishbucks'] = fishbucks
            if fishcoins is not None:
                update_data['fishcoins'] = fishcoins
            player.change(**update_data).commit()
            return ServiceResponse(True, data=player)
        return ServiceResponse(False, message="Player not found.")

    def add_experience(self, player_id, xp_amount):
        player = Player.get(player_id)
        if player:
            new_xp = player.xp + xp_amount
            new_level = (new_xp // 1000) + 1
            update_data = {'xp': new_xp}
            if new_level > player.level:
                update_data['level'] = new_level
            player.change(**update_data).commit()
            return ServiceResponse(True, data=player)
        return ServiceResponse(False, message="Player not found.")

    def get_player_stats(self, player_id):
        player = Player.get(player_id)
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
