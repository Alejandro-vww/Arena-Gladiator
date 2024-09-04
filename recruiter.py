import time
from evaluator import Evaluator
from game_dict import GameDict

game_dict = GameDict()


class Recruiter:

    def play_card(self, cards, *election):
        raise NotImplementedError("This method must be implemented by the subclass.")
    
    def play_land(self):
        self.play_card(list(card for card in game_dict.instances.hand if card.is_land))
        
    def play_optimized_cards(self):
        for card in Evaluator.optimize():
            self.play_card(card)
            time.sleep(1)
            game_dict.wait()

