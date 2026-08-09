from game.game_objects.cards.base import Base


class Land(Base):

    @property
    def is_land(self):
        return True if 'CardType_Land' in self.dictionary.get('cardTypes', []) else False
