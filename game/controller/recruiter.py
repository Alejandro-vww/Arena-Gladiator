import time

from game.controller.game_actions import GameActions
from evaluator import Evaluator
from game.game import GameDict

game_dict = GameDict()


class Recruiter(GameActions):

    def play_land(self):
        self.play_cards(list(card for card in game_dict.hand if card.is_land))
        
    def play_optimized_cards(self, use_treasures=False):
        mana = game_dict.untapped_lands
        if use_treasures:
            mana += game_dict.untapped_treasures
        for card in Evaluator.optimize():
            self.play_cards(card)
            time.sleep(1)
            game_dict.wait_action()

    def play_optimized_creatures(self, use_treasures=False):
        creatures = list(card for card in game_dict.hand if card.is_creature)
        mana = game_dict.untapped_lands
        if use_treasures:
            mana += game_dict.untapped_treasures
        for card in Evaluator.optimize(hand=creatures):
            self.play_cards(card)
            time.sleep(1)
            game_dict.wait_action()

