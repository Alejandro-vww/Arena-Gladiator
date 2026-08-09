import pydirectinput
import time

from game.game import GameDict
from exceptions import EscPressedError
from game.game_window.coordinates import Coordinates

pydirectinput.PAUSE = 0


class GameActions:
    _listeners_started = False

    def __init__(self, game=None, window=None, coord=None, central_unit_module=None):
        self.game = game or GameDict()
        self.cards_location = {}

        from game.game_window.window import Window
        self.window = window or Window()
        self.coord = coord or Coordinates(self.window)

        if central_unit_module is None:
            import central_unit
            central_unit_module = central_unit
        self.central_unit = central_unit_module

        if not GameActions._listeners_started:
            self.central_unit.start_listeners()
            GameActions._listeners_started = True

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
            if self.game.cursor != last_cursor:  # Change in cursor
                if last_cursor is not None:  # Cursor leaving an instance
                    dictionary[last_cursor.grp_id] = int((beginning + x_pos) / 2)
                    beginning = x_pos
                else:
                    beginning = x_pos
                last_cursor = self.game.cursor
            x_pos += jump

    def scan_hand(self):
        self.scan(self.coord.left_hand, self.coord.right_hand, self.coord.height_hand, self.cards_location)

    def play_cards(self, cards, *election):
        if not isinstance(cards, list):
            cards = [cards]

        for card in cards:
            if card not in self.game.hand or not self.select_card(card):
                continue
            time.sleep(0.3)
            if self.game.cursor == card:
                pydirectinput.mouseDown()
                time.sleep(0.2)
                pydirectinput.move(0, self.coord.scale_y_1080p(-900))
                time.sleep(0.2)
                pydirectinput.mouseUp()
                return True
        return False

    def select_card(self, card):
        if card not in self.game.hand:
            return False
        for _ in range(3):
            if int(card) in self.cards_location.keys():
                center = self.cards_location.pop(int(card))
                x_coord = self.coord.x_coord_generator(self.coord.left_hand, self.coord.right_hand, 30, center=center)
            else:
                x_coord = self.coord.x_coord_generator(self.coord.left_hand, self.coord.right_hand, 30)

            for i in range(30):
                self.move_to(next(x_coord), self.coord.height_hand)
                if self.game.cursor == card:
                    return True
        print('The card was not found')
        return False

    # Generator
    def move_to_creatures(self, card_list):
        if not isinstance(card_list, list):
            card_list = [card_list]
        # grpId/instance compatibility
        try:
            instance_ids = list(card.instance_id for card in card_list)
        except AttributeError:
            card_list_inst = list(card for card in self.game.hero_battlefield if card in card_list)
            instance_ids = list(card.instance_id for card in card_list_inst)

        for x in range(1701, 200, -50):
            self.move_to(self.coord.scale_x_1080p(x), self.coord.scale_y_1080p(590))
            time.sleep(0.4)
            instance_id = self.game.cursor.instance_id if self.game.cursor else None
            if self.game.cursor and instance_id in instance_ids:
                instance_ids.remove(instance_id)
                yield

            if not instance_ids:
                break

    # LOW LEVEL MOUSE & KEYBOARDS FUNCTIONS

    def move_to(self, x, y, check=True):
        if self.central_unit.stop:
            self.central_unit.stop = False
            raise EscPressedError
        if check:
            pydirectinput.moveTo(x + self.window.left, y + self.window.top)
        else:
            pydirectinput.moveTo(x + self.window.unchecked_left, y + self.window.unchecked_top)
        time.sleep(0.2)


    def move(self, x, y):
        if self.central_unit.stop:
            raise EscPressedError
        pydirectinput.move(self.coord.scale_x_1080p(x), self.coord.scale_y_1080p(y))
        time.sleep(0.2)

    def click(self):
        if self.central_unit.stop:
            raise EscPressedError
        pydirectinput.mouseDown()
        time.sleep(0.1)
        pydirectinput.mouseUp()

    def space(self):
        if self.central_unit.stop:
            raise EscPressedError
        self.window.check_status()
        pydirectinput.keyDown("space")
        time.sleep(0.1)
        pydirectinput.keyUp("space")

    def escape(self):
        if self.central_unit.stop:
            raise EscPressedError
        pydirectinput.keyDown("escape")
        time.sleep(0.1)
        pydirectinput.keyUp("escape")


