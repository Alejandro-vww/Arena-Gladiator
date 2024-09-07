import time

from aplication_status import AplicationStatus
from evaluator import Evaluator
from game_dict import GameDict
from game_window.executor import Executor
from evaluator import Evaluator
from instances.card import Card


game_dict = GameDict()
app_status = AplicationStatus()
execute = Executor()

class DefaultMode:
    @staticmethod
    def mulligan():
        if game_dict.active and app_status.mulligan:
            if game_dict.mulligan_count == 0:
                if 2 <= len(list(card for card in game_dict.instances.hand if card.is_land)) <= 4:
                    execute.space()
                else:
                    execute.mulligan()
            elif game_dict.mulligan_count == 1:
                execute.space()
                time.sleep(1)
                if len(list(card for card in game_dict.instances.hand if card.is_land)) > 3:
                    execute.mulligan_discard(0, position=True)
                else:
                    execute.mulligan_discard(6, position=True)

    @staticmethod
    def play_land():
        execute.play_card(list(card for card in game_dict.instances.hand if card.is_land))

    @staticmethod
    def main_phase_1():
        execute.play_optimized_cards()
        game_dict.wait_reading()
        if not Evaluator.optimize():
            return 'Phase_Combat'

    @staticmethod
    def declare_attackers():
        execute.attack_if_kill()

    @staticmethod
    def main_phase_2():
        execute.space()




