from instances.land import Land
from instances.creature import Creature
from instances.planeswalker import Planeswalker


class Card(Land, Creature, Planeswalker):

    @property
    def cost_RGBWBN(self):
        try:
            return sum(coste['count'] for coste in self._dictionary.get('manaCost'))
        except KeyError:
            return None
        except Exception as e:
            print(f'Error Card cost_RGBWBN: {e}')
            return None
    @property
    def sum_cost(self):
        try:
            return sum(coste['count'] for coste in self._dictionary.get('manaCost'))
        except KeyError:
            return None
        except Exception as e:
            print(f'Error Card sum_cost: {e}')
            return None


    @property
    def planeswalker(self):
        try:
            return True if 'CardType_Planeswalker' in self._dictionary.get('cardTypes') else False
        except KeyError:
            print('Card property planeswalker KeyWord')
            return None


    # @property
    #     mana_cost


if __name__ == '__main__':
    a = Card('hola')
