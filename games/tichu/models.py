import json

from django.db import models

DEF_MAX_LENGTH = 255

class JSONField(models.TextField):
    """A class providing interface for saving JSON in database.

    Uses json.dumps to database and json.loads from it.
    That means, don't waste time converting objects to JSON, as it is done by
    this field.
    """
    def db_type(self, connection):
        return 'text'

    def from_db_value(self, value, expression, connection, context):
        return json.loads(value)

    def to_python(self, value):
        if isinstance(value, str):
            return json.loads(value)
        return value

    def get_prep_value(self, value):
        return json.dumps(value)


class Game(models.Model): pass


class StateType(models.Model):
    title = models.CharField(max_length=DEF_MAX_LENGTH)
    long_description = models.TextField(blank=True)


class GameState(models.Model):
    game = models.ForeignKey(Game, blank=True)
    state_type = models.ForeignKey(StateType)
    notes = models.TextField(blank=True)


class CardGameState(GameState):
    hands = JSONField()
    last_played = JSONField()


class TichuGameState(CardGameState):
    tichu = JSONField()
    grand_tichu = JSONField()


class AlternativeGameState(GameState):
    original = models.ForeignKey(GameState)


class AlternativeTichuGameState(AlternativeGameState, TichuGameState): pass
