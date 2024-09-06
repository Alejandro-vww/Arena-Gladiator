import time
from itertools import product
import numpy as np
import traceback

from turn_info import TurnInfo


class GameDict(TurnInfo):
    _instance = None
    started = False

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not self.started:
            from instances.instances import Instances
            from aplication_status import AplicationStatus
            self.started = True

            self.username = None
            self.status = AplicationStatus()
            self.game_state = {}
            self.other_dicts = {}
            self.game_room_info = {}
            self.instances = Instances()
            self.UI_state = {}
            self.client_2_match = {}

            self.last_actualization = None

    @property
    def hero_seat_id(self):
        if players := self.game_room_info.get('gameRoomInfo', {}).get('players'):
            if players[0].get('playerName') == self.username:
                return players[0].get('teamId')
            if players[1].get('playerName') == self.username:
                return players[1].get('teamId')

    @property
    def villain_seat_id(self):
        if players := self.game_room_info.get('gameRoomInfo', {}).get('players'):
            if players[0].get('playerName') == self.username:
                return players[1].get('teamId')
            if players[1].get('playerName') == self.username:
                return players[0].get('teamId')

    @property
    def game_objects(self):
        return self.game_state.get('gameObjects', [])


    @property
    def actions(self):
        actions = self.other_dicts.get('GREMessageType_ActionsAvailableReq', {})
        if self.game_state_id >= actions.get('gameStateId', 0):
            return actions.get('actionsAvailableReq', {}).get('actions', [])
        else:
            return []

    @property
    def mana_actions(self):
        return list(action for action in self.actions if action.get('actionType') == 'ActionType_Activate_Mana')

    @property
    def game_state_id(self):
        return self.game_state.get('gameStateId', 0)

    @property
    def cursor(self):
        instance_id = self.UI_state.get('payload', {}).get('uiMessage', {}).get('onHover', {}).get('objectId')
        return self.instances.num(instance_id)

    @property
    def request_id(self):
        return self.UI_state.get('requestId')

    @property
    def mulligan_count(self):
        for player in self.game_state.get('players', []):
            if player.get('teamId') == self.hero_seat_id:
                return player.get('mulliganCount', 0)

    @property
    def can_play_land(self):
        return 'ActionType_Play' in set(action.get('actionType') for action in self.actions)

    # Mana
    @property
    def mana(self):
        mana_dic = {}
        mana_names = ['ManaColor_Red', 'ManaColor_Green', 'ManaColor_Blue', 'ManaColor_White', 'ManaColor_Black',
                      'ManaColor_Colorless']
        if approximation := len(self.mana_actions) > 7:
            return [(approximation, approximation, approximation, approximation, approximation, approximation)]

        for action in self.mana_actions:
            inst_id = action.get('instanceId')
            if inst_id not in mana_dic.keys():  # Creamos un diccionario con key el instanceId y valor una lista con las distintas opciones de maná que ofrece
                mana_dic[inst_id] = []
            for option in action.get('manaPaymentOptions', []):
                total_mana = [0, 0, 0, 0, 0, 0]  # R, G, B ,W, Negro, incoloro
                for mana in option.get('mana', []):
                    total_mana[mana_names.index(mana.get('color'))] += 1
                mana_dic[inst_id].append(total_mana)
        mana_combinations = list(product(*list(mana_dic.values())))
        options = list(sum(np.array(mana_vector) for mana_vector in combination) for combination in mana_combinations if combination)         # cada opción contiene una combinación de los posibles vectores RGBWBN que pueden dar las tierras bajadas, su suma y set dará las posibles combinaciones de maná
        options = set(tuple(mana_vector) for mana_vector in options)  # cada opción contiene una combinación de los posibles vectores RGBWBN que pueden dar las tierras bajadas, su suma y set dará las posibles combinaciones de maná
        options = list(int(numpy_int) for vector in options for numpy_int in vector)
        return options if options else [0, 0, 0, 0, 0, 0]

    def wait(self):
        time.sleep(0.4)
        while not self.active and self.status.screen == 'Playing' or time.time() - self.last_actualization < 1.5:
            time.sleep(0.5)

    def wait_reading(self):
        while time.time() - self.last_actualization < 0.3:
            time.sleep(0.15)

