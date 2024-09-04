import pydirectinput
import time
import game_dict
from game_window.coordinates import Coordinates
from log_reader import LogReader
from data_base.data_manager import grp_id_order
from recruiter import Recruiter
from field_marshal import FieldMarshal

pydirectinput.PAUSE = 0


class Executor(Recruiter, FieldMarshal):
    _instance = None
    _started = False

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._started:
            self.game_dict = game_dict.GameDict()
            self.cards_location = {}
            self._started = True
            from game_window.window import Window
            self.window = Window()
            self.coord = Coordinates(self.window)

    def start_game(self):
        time_limit = 5 * 60
        starting_time = time.time()
        while self.window.status.screen != 'Playing' and time.time() - starting_time < time_limit:
            self.move_to(*self.coord.start_button)
            self.click()
            time.sleep(0.5)

    def cancel(self):
        self.move_to(*self.coord.cancel_button)
        time.sleep(0.2)
        self.click()

    def concede(self):
        self.move_to(*self.coord.config_button, check=False)
        time.sleep(0.2)
        self.click()
        time.sleep(0.8)
        self.move_to(*self.coord.concede_button, check=False)
        time.sleep(0.2)
        self.click()

    def scan(self, start, end, height, dictionary):
        jump = (end - start) / 60
        last_cursor = None
        dictionary.clear()
        beginning = x_pos = start
        for _ in range(61):
            self.move_to(int(x_pos), height)
            time.sleep(0.075)
            if self.game_dict.cursor != last_cursor:  # Change in cursor
                if last_cursor is not None:  # Cursor leaving an instance
                    dictionary[last_cursor.grp_id] = int((beginning + x_pos) / 2)
                    beginning = x_pos
                else:
                    beginning = x_pos
                last_cursor = self.game_dict.cursor
            x_pos += jump

    def scan_hand(self):
        self.scan(self.coord.left_hand, self.coord.right_hand, self.coord.height_hand, self.cards_location)

    def play_card(self, cards, *election):
        if not isinstance(cards, list):
            cards = [cards]

        for card in cards:
            if card not in self.game_dict.instances.hand or not self.select_card(card):
                continue
            time.sleep(0.3)
            if self.game_dict.cursor == card:
                pydirectinput.mouseDown()
                time.sleep(0.2)
                pydirectinput.move(0, self.coord.scale_y_1080p(-900))
                time.sleep(0.2)
                pydirectinput.mouseUp()
                return True
        return False

    def select_card(self, card):
        if card not in self.game_dict.instances.hand:
            return False
        for _ in range(3):
            if int(card) in self.cards_location.keys():
                center = self.cards_location.pop(int(card))
                x_coord = self.coord.x_coord_generator(self.coord.left_hand, self.coord.right_hand, 30, center=center)
            else:
                x_coord = self.coord.x_coord_generator(self.coord.left_hand, self.coord.right_hand, 30)

            for i in range(30):
                self.move_to(next(x_coord), self.coord.height_hand)
                time.sleep(0.45)
                if self.game_dict.cursor == card:
                    return True
        print('The card was not found')
        return False

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
            last_cursor = self.game_dict.request_id
            card_selected_position = 0

            for _ in range(35):
                time.sleep(0.07)
                self.move(35, 0)
                if last_cursor != self.game_dict.request_id:
                    last_cursor = self.game_dict.request_id
                    card_selected_position += 1
                    if card_selected_position > position:
                        for _ in range(5):
                            time.sleep(0.07)
                            self.move(-35, 0)
                            if last_cursor != self.game_dict.request_id:
                                self.move(-20, 0)
                                discard()
                                return
                    if card_selected_position == position:
                        self.move(20, 0)
                        discard()
                        return
            print('card not found')

        hand = self.game_dict.instances.hand
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

    # LOW LEVEL MOUSE & KEYBOARDS FUNCTIONS

    def move_to(self, x, y, check=True):
        if check:
            pydirectinput.moveTo(x + self.window.left, y + self.window.top)
        else:
            pydirectinput.moveTo(x + self.window.unchecked_left, y + self.window.unchecked_top)

    def move(self, x, y):
        pydirectinput.move(self.coord.scale_x_1080p(x), self.coord.scale_y_1080p(y))
        time.sleep(0.2)

    def click(self):
        pydirectinput.mouseDown()
        time.sleep(0.2)
        pydirectinput.mouseUp()

    def space(self):
        self.window.check_status()
        pydirectinput.keyDown("space")
        time.sleep(0.2)
        pydirectinput.keyUp("space")

    def escape(self):
        pydirectinput.keyDown("escape")
        time.sleep(0.2)
        pydirectinput.keyUp("escape")


if __name__ == '__main__':
    LogReader.start_read()
    e = Executor()
    e.start_game()
