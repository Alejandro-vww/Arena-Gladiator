from instances.instances import Instances
from turn_info import TurnInfo


class GameDict(TurnInfo, Instances):

    @property
    def cursor(self):
        instance_id = self.UI_state.get('payload', {}).get('uiMessage', {}).get('onHover', {}).get('objectId')
        return self.num(instance_id)

