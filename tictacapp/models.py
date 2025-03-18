from django.db import models
from django.contrib.auth.models import User
import uuid

class Game(models.Model):
    room_code = models.UUIDField(default=uuid.uuid4, unique=True, db_index=True)
    winner = models.ForeignKey(User, related_name='won_games', null=True, blank=True, on_delete=models.SET_NULL)
    current_turn = models.ForeignKey(User, related_name='current_turn_games', null=True, blank=True, on_delete=models.SET_NULL)
    board_state = models.CharField(max_length=9, default=' ' * 9)  # Representing the board as a string of 9 characters

    def __str__(self):
        return f"Game {self.room_code}"

class Player(models.Model):
    game = models.ForeignKey(Game, related_name='players', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='games', on_delete=models.CASCADE)
    symbol = models.CharField(max_length=1)  # 'X' or 'O'

    def __str__(self):
        return f"{self.user.username} ({self.symbol}) in {self.game.room_code}"

class Move(models.Model):
    game = models.ForeignKey(Game, related_name='moves', on_delete=models.CASCADE)
    player = models.ForeignKey(Player, related_name='moves', on_delete=models.CASCADE)
    position = models.IntegerField()  # Position on the board (0-8)

    def __str__(self):
        return f"Move by {self.player.user.username}"