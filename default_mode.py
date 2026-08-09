import time

from game.aplication_status import AplicationStatus
from game.game import GameDict
from game.controller.executor import Executor
from evaluator import Evaluator

game_dict = GameDict()
app_status = AplicationStatus()
execute = Executor()

class DefaultMode:
    @staticmethod
    def mulligan():
        if game_dict.active and app_status.mulligan:
            if game_dict.mulligan_count == 0:
                if 2 <= len(list(card for card in game_dict.hand if card.is_land)) <= 4:
                    execute.space()
                else:
                    execute.mulligan()
            elif game_dict.mulligan_count == 1:
                execute.space()
                time.sleep(1)
                if len(list(card for card in game_dict.hand if card.is_land)) > 3:
                    execute.mulligan_discard(0, position=True)
                else:
                    execute.mulligan_discard(6, position=True)

    @staticmethod
    def play_land():
        execute.play_cards(list(card for card in game_dict.hand if card.is_land))

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
        return 'End_Turn'




