import time

from game.game_objects.instances import Instances
from game.turn_info import TurnInfo


class GameDict(TurnInfo, Instances):

    @property
    def cursor(self):
        self.wait_reading()
        instance_id = self.UI_state.get('payload', {}).get('uiMessage', {}).get('onHover', {}).get('objectId')
        return self.num(instance_id)

    @property
    def autopay(self):
        pay_cost_request = self.other_dicts.get('GREMessageType_PayCostsReq', {})
        if self.game_state_id > pay_cost_request.get('gameStateId', 0) or self.game_state_id == 0:
            return 'nada que pagar'
        if 'autoTapActionsReq' in pay_cost_request.get('payCostsReq', {}).keys():
            return 'can auto tap'
        else:
            return 'cant auto tap'