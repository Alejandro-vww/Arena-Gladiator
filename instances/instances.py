from game_dictionaries import GameDictionaries
from instances.card import Card


class Instances(GameDictionaries):

    def __init__(self):
        super().__init__()
        self._instances = {}        # {inst_num: Card_obj}
        self._game_state_id_inst = 0

    def _update(self):
        for inst in self.game_objects:
            self._instances[inst.get('instanceId')] = Card(inst)
        self._game_state_id_inst = self.game_state_id

    def reset_instances(self):
        self._instances = {}
        self._game_state_id_inst = 0

    def num(self, inst_no):
        if self.game_state_id > self._game_state_id_inst:
            self._update()
        return self._instances.get(inst_no, Card({}))

    def zone(self, zone_number):
        for zone in self.game_state.get('zones', []):
            if zone.get('zoneId') == zone_number:
                return list(self.num(card) for card in zone.get('objectInstanceIds', []))
        return []

    @property
    def hand(self):
        if hero_seat := self.hero_seat_id:
            return self.zone(27 + hero_seat * 4) + self.commander
        return []

    @property
    def commanders(self):
        return self.zone(26)

    @property
    def commander(self):
        return list(commander for commander in self.commanders if commander.owned)

    @property
    def battlefield(self):
        return self.zone(28)

    @property
    def hero_battlefield(self):
        return list(card for card in self.battlefield if card.owned)

    @property
    def villain_battlefield(self):
        return list(card for card in self.battlefield if not card.owned)

    @property
    def hero_army(self):
        return list(card for card in self.hero_battlefield if card.is_creature)

    @property
    def offensive_army(self):
        return list(minion for minion in self.hero_army if minion.attack_ready)

    @property
    def defensive_army(self):
        return list(minion for minion in self.hero_army if not minion.tapped)

    @property
    def villain_army(self):
        return list(card for card in self.villain_battlefield if card.is_creature)

    @property
    def villain_offensive_army(self):
        return list(minion for minion in self.villain_army if minion.attack_ready)

    @property
    def villain_defensive_army(self):
        return list(minion for minion in self.villain_army if not minion.tapped)

    @property
    def untapped_lands(self):
        return len(list(card for card in self.hero_battlefield if card.is_land and not card.tapped))

    @property
    def complete_stack(self):
        return self.zone(27)

    @property
    def stack(self):
        return self.complete_stack[0] if self.complete_stack else None
