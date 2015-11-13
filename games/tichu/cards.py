import functools

from . import (
    constants,
    utils,
    )

class Card():
    def __init__(self, kind=None, strength=None, value=None, verbose=None, **kwargs):
        if kind is None:
            raise(TypeError("Missing required 'kind' argument."))
        self.kind = kind
        self.strength = strength
        self.value = value
        self.verbose = verbose if verbose is not None else kind
        super().__init__(**kwargs)

    def __valid_comparision(self, arg):
        return hasattr(arg, "kind") and hasattr(arg, "strength")

    _valid_comparision = __valid_comparision

    def __lt__(self, value):
        if not  self.__valid_comparision(value):
            return NotImplemented
        if self.strength is not None:
            if value.strength is not None:
                return self.strength < value.strength
            else:
                return False
        elif value.strength is not None:
            return True
        return self.kind < value.kind

    def __str__(self):
        return self.kind


class SimpleCard(Card):
    def __init__(self, colour=None, kind=None, strength=None, **kwargs):
        if colour is None:
            raise(TypeError("Missing required 'colour' argument."))
        self.colour = colour
        if kind is None:
            if strength is not None:
                kind = str(strength)
        super().__init__(kind=kind, strength=strength, **kwargs)

    def __valid_comparision(self, arg):
        if super()._valid_comparision(arg):
            if hasattr(arg, "colour") and (arg.colour is not None):
                if arg.strength is not None:
                    return True
        return False

    _valid_comparision = __valid_comparision

    def __lt__(self, value):
        if not self.__valid_comparision(value):
            return super().__lt__(value)
        if self.strength < value.strength:
            return True
        if self.strength == value.strength:
            return self.colour < value.colour
        return False

    def __eq__(self, value):
        if not self._valid_comparision(value):
            return False
        if (self.strength == value.strength) and (self.colour == value.colour):
            return True

    def __str__(self):
        return self.kind + self.colour[0]


class MahJongg(Card):
    def __init__(self):
        super().__init__(kind='1', strength=1)

class Dragon(Card):
    def __init__(self):
        super().__init__(kind='R', value=25, verbose="Dragon")

class Pheonix(Card):
    def __init__(self):
        super().__init__(kind='P', value=-25, verbose="Pheonix")

class Dog(Card):
    def __init__(self):
        super().__init__(kind="D", verbose="Dog")


