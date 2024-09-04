from instances.spell import Spell


class Planeswalker(Spell):

    @property
    def is_planeswalker(self):
        return True if 'CardType_Planeswalker' in self._dictionary.get('cardTypes', []) else False
