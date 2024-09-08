import time

from game import GameDict
from minion_of_the_mighty import MinionOfTheMighty
from game_window.executor import Executor

game_dict = GameDict()
execute = Executor()


class Zone27:

    @staticmethod
    def solve(grp_id):
        if grp_id == 143798:    #Select dragon to cast free
            hand = game_dict.hand
            battlefield = game_dict.hero_battlefield
            legendary_dragons_played = list(card for card in battlefield if card.is_dragon and card.is_legendary)
            dragons = list(card for card in hand if card.is_dragon and card not in legendary_dragons_played)
            dragons.sort(key=MinionOfTheMighty.dragon_value, reverse=True)

            if dragons and execute.select_card(dragons[0]):
                time.sleep(0.3)
                execute.click()
                execute.space()

        elif grp_id == 91091:    #Select Niv-Mizzet damage objective
            execute.move_to(*execute.coord.villain)
            time.sleep(0.1)
            execute.click()

        else:
            execute.space()

