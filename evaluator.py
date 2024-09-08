from itertools import permutations
from game import GameDict

game_dict = GameDict()


class Evaluator:

    @staticmethod
    def card_value(card):
        hand = game_dict.hand
        battlefield = game_dict.hero_battlefield
        max_card_cost = max(card.mana_cost for card in hand)
        total_mana = len(list(card for card in hand + battlefield if card.is_land))
        if total_mana > max_card_cost and card.is_land:
            return -10
        elif card.mana_cost > total_mana:
            return card.mana_cost - total_mana
        return card.mana_cost

    @staticmethod
    def optimize(mana=None, hand=None, evaluation_function=None, penalization_function=None):
        if not mana:
            mana = game_dict.untapped_lands
        if not hand:
            hand = list(card for card in game_dict.hand if not card.is_land)
        if not evaluation_function:
            evaluation_function = Evaluator.card_value

        cost_permutations = []
        cards_permutations = []

        for i in range(len(hand)):
            cost_permutations.extend(list(permutations(list(card.mana_cost for card in hand), len(hand) - i)))
            cards_permutations.extend(list(permutations(hand, len(hand) - i)))

        best_value = 0
        optimized_cards = []

        for costs, cards in zip(cost_permutations, cards_permutations):
            if sum(costs) <= mana:
                value = sum(evaluation_function(card) for card in cards)
                if penalization_function:
                    value -= penalization_function(sum(costs))
                if value > best_value:
                    optimized_cards = list(cards)
                    best_value = value

        return optimized_cards


if __name__ == '__main__':
    pass
