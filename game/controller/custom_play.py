import time

from game.controller.game_actions import GameActions
from game.game import GameDict
from data_base.names_database import *


class CustomPlay(GameActions):

    def play_custom_color_land(self, card, color):
        if card == red_green_pathway:
            self.play_red_green_pathway(card, color)

        elif card == temple_of_the_dragon:
            self.play_temple_of_the_dragon(card, color)

        elif card == stomping_ground:
            self.play_stomping_ground(card)

        else:
            self.play_cards(card)

    def play_stomping_ground(self, card):
        self.play_cards(card)
        time.sleep(0.7)
        self.select_left_option()

    def play_temple_of_the_dragon(self, card, color):
        self.play_cards(card)
        time.sleep(1)
        if dragon := list(card for card in self.game.hand if card.is_dragon):
            self.select_card(dragon[0])
            time.sleep(0.4)
            if self.game.cursor.is_dragon:
                self.click()
                time.sleep(0.15)
                self.space()
        self.select_five_color_option(color)

    def play_red_green_pathway(self, card, color):
        self.play_cards(card)
        time.sleep(0.5)
        if color == 'red':
            self.select_left_card_option()
        elif color == 'green':
            self.select_right_card_option()
        else:
            print('wrong color')
            self.select_right_card_option()

    def cast_on(self, card, instance, option=None):
        self.play_cards(card)
        time.sleep(1)
        if option == 'right':
            self.select_right_card_option()
        elif option == 'left':
            self.select_left_card_option()
        elif option == 'center':
            print('to be implemented')
        next(self.move_to_creatures(instance))
        time.sleep(0.3)
        self.click()

    def select_left_card_option(self):
        self.move_to(*self.coord.left_card_option)
        time.sleep(2)
        self.click()

    def select_right_card_option(self):
        self.move_to(*self.coord.right_card_option)
        time.sleep(2)
        self.click()

    def select_left_option(self):
        self.move_to(*self.coord.left_option)
        time.sleep(2)
        self.click()

    def select_right_option(self):
        self.move_to(*self.coord.right_option)
        time.sleep(2)
        self.click()

    def select_five_color_option(self, color):
        self.move_to(*self.coord.five_color_option(color))
        time.sleep(2)
        self.click()


