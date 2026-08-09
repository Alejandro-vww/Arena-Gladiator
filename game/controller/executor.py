import pydirectinput
import time

from game.controller.custom_play import CustomPlay
from data_base.data_manager import grp_id_order
from game.controller.recruiter import Recruiter
from game.controller.combat_actions import CombatActions

pydirectinput.PAUSE = 0


class Executor(Recruiter, CombatActions, CustomPlay):

    def mulligan(self):
        self.move_to(*self.coord.mulligan_button)
        time.sleep(0.1)
        self.click()

    def mulligan_discard(self, cards, position=False):
        def discard():
            time.sleep(0.2)
            pydirectinput.mouseDown()
            time.sleep(0.2)
            pydirectinput.move(-2, 0)
            time.sleep(0.2)
            pydirectinput.move(-5, 0)
            time.sleep(0.2)
            self.move_to(self.coord.scale_x_1080p(233), self.coord.scale_y_1080p(550))
            time.sleep(0.1)
            pydirectinput.mouseUp()

        def discard_position(position):
            self.move_to(self.coord.scale_x_1080p(860), self.coord.scale_x_1080p(550))
            last_cursor = self.game.request_id
            card_selected_position = 0

            for _ in range(35):
                time.sleep(0.07)
                self.move(35, 0)
                if last_cursor != self.game.request_id:
                    last_cursor = self.game.request_id
                    card_selected_position += 1
                    if card_selected_position > position:
                        for _ in range(5):
                            time.sleep(0.07)
                            self.move(-35, 0)
                            if last_cursor != self.game.request_id:
                                self.move(-20, 0)
                                discard()
                                return
                    if card_selected_position == position:
                        self.move(20, 0)
                        discard()
                        return
            print('card not found')

        hand = self.game.hand
        hand.sort(key=grp_id_order)
        if not isinstance(cards, list):
            cards = [cards]
        if position:
            cards.sort(reverse=True)  # Discard from right to left so position won't be altered
        for card in cards:
            if position:
                discard_position(card)
            elif card in hand:
                discard_position(hand.index(card))
                hand.remove(card)
            else:
                discard_position(1)
                hand.pop(1)
            time.sleep(0.3)
        self.space()
        time.sleep(1)
