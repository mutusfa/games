import json

from django.core.exceptions import ValidationError
from django.db import models

from .card_pass import parse_hands


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


class HandsField(JSONField):
    def from_db_value(self, value, expression, connections, context):
        return parse_hands(
            super().from_db_value(value, expression, connections, context)
            )

    def to_python(self, value):
        return parse_hands(
            super().to_python(value)
            )


class Game(models.Model): pass


class StateType(models.Model):
    title = models.CharField(max_length=DEF_MAX_LENGTH)
    long_description = models.TextField(blank=True)


class GameState(models.Model):
    game = models.ForeignKey(Game, blank=True)
    state_type = models.ForeignKey(StateType)
    notes = models.TextField(blank=True)

    class Meta():
        abstract = True


class CardGameState(GameState):
    hands = HandsField()
    last_played = JSONField()

    class Meta(GameState.Meta):
        abstract = True


class TichuGameState(CardGameState):
    tichu = JSONField()
    grand_tichu = JSONField()


class AlternativeTichuGameState(TichuGameState):
    original = models.ForeignKey('self')
