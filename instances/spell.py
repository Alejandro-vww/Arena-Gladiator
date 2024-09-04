from instances.base import Base


class Spell(Base):

    @property
    def mana_cost(self):
        return sum(cost.get('count', 0) for cost in self.related_action.get('manaCost', []))


    @property
    def cost_RGBWBN(self):
        pass

