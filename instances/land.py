from instances.base import Base


class Land(Base):

    @property
    def is_land(self):
        return True if 'CardType_Land' in self._dictionary.get('cardTypes', []) else False
