from data_base.names_database import grpid_names


class Base:
    game_dict = None

    def __init__(self, dictionary):
        self._dictionary = dictionary
        if not Base.game_dict:
            from game import GameDict
            Base.game_dict = GameDict()

    def __eq__(self, other):
        return self.grp_id == other

    def __str__(self):
        return str(grpid_names.get(self.grp_id, self.grp_id))

    def __repr__(self):
        return str(grpid_names.get(self.grp_id, self.grp_id))

    def __int__(self):
        return int(self.grp_id)

    @property
    def instance_id(self):
        return self._dictionary.get('instanceId')
    @property
    def grp_id(self):
        return self._dictionary.get('grpId')

    @property
    def related_action(self):
        actions = list(action.get('action', {}) for action in self.game_dict.game_state.get('actions', []))
        return next((action for action in actions if action.get('instanceId') == self.instance_id), {})

    @property
    def owner(self):
        return self._dictionary.get('ownerSeatId')

    @property
    def owned(self):
        return self.owner == self.game_dict.hero_seat_id

    @property
    def zone_id(self):
        return self._dictionary.get('zoneId')

    @property
    def tapped(self):
        return True if 'isTapped' in self._dictionary.keys() else False