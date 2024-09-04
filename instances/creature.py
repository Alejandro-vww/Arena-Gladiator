from instances.spell import Spell

class Creature(Spell):


    @property
    def is_creature(self):
        return True if 'CardType_Creature' in self._dictionary.get('cardTypes', []) else False

    @property
    def power(self):
        return self._dictionary.get('power', {}).get('value', 0)

    @property
    def toughness(self):
        try:
            if 'value' in self._dictionary['toughness'].keys():
                return self._dictionary.get('toughness').get('value')
            else:
                print('Class Card: no toughness??')
                return 0
        except Exception as e:
            print(f'Excepción property toughness {e}')
    @property
    def stats_4(self):
        if self.first_strike:
            stats =  [self.power, 0 , self.toughness]
        elif self.double_strike:
            stats =  [self.power,self.power,self.toughness]
        else:
            stats =  [0,self.power,self.toughness]

        if self.death_touch:
            return [stats[0], stats[1], stats[2],True]
        else:
            return [stats[0], stats[1], stats[2],False]



    @property
    def summoning_sickness(self):
        return True if 'hasSummoningSickness' in self._dictionary.keys() else False
    @property
    def attack_ready(self):
        if not self.tapped and not self.defender:
            if not self.summoning_sickness or self.haste:
                return True
        return False

    @property
    def haste(self):
        return True if 9 in self._dictionary.get('abilities', []) else False

    @property
    def defender(self):
        return True if 2 in self._dictionary.get('abilities', []) else False

    @property
    def first_strike(self):
        return True if 6 in self._dictionary.get('abilities', []) else False

    @property
    def double_strike(self):
        return True if 3 in self._dictionary.get('abilities', []) else False

    @property
    def death_touch(self):
        return True if 1 in self._dictionary.get('abilities', []) else False

    @property
    def fly(self):
        return True if 8 in self._dictionary.get('abilities', []) else False






    @property
    def attack_declared(self):
        try:
            return True if self._dictionary.get('attackState') == 'AttackState_Declared' else False
        except KeyError:
            return None
    @property
    def attacking(self):
        try:
            return True if self._dictionary.get('attackState') == 'AttackState_Attacking' else False
        except KeyError:
            return None

    @property
    def block_declared(self):
        try:
            return True if self._dictionary.get('attackState') == 'BlockState_Declared' else False
        except KeyError:
            return None
    @property
    def blocking(self):
        try:
            return True if self._dictionary.get('attackState') == 'BlockState_Blocking' else False
        except KeyError:
            return None
    @property
    def blocked(self):
        try:
            return True if self._dictionary.get('attackState') == 'BlockState_Blocked' else False
        except KeyError:
            return None
    @property
    def unblocked(self):
        try:
            return True if self._dictionary.get('attackState') == 'BlockState_Unblocked' else False
        except KeyError:
            return None


    @property
    def is_legendary(self):
        return True if 'SuperType_Legendary' in self._dictionary.get('superTypes', []) else False

    @property
    def is_dragon(self):
        return True if 'SubType_Dragon' in self._dictionary.get('subtypes', []) else False

    @property
    def is_goblin(self):
        try:
            return True if self.is_creature and "SubType_Goblin" in self._dictionary.get('subtypes') else False
        except KeyError:
            print('Card property creature KeyWord')
            return None

