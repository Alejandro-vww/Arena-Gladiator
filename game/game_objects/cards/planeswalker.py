from game.game_objects.cards.spell import Spell


class Planeswalker(Spell):

    @property
    def is_planeswalker(self):
        return True if 'CardType_Planeswalker' in self.dictionary.get('cardTypes', []) else False
