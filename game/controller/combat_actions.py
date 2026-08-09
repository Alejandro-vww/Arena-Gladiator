import time

from game.controller.game_actions import GameActions
from game.game import GameDict

game_dict = GameDict()


class CombatActions(GameActions):
    coord = None
    game = None

    def check_declared_attackers(self, attack_command):
        sorted_attack_command = sorted(attack_command, key=lambda instance: instance.instance_id)
        sorted_attackers = sorted(self.attack_declared_creatures, key=lambda instance: instance.instance_id)
        return sorted_attack_command == sorted_attackers

    @property
    def attack_declared_creatures(self):
        return list(creature for creature in game_dict.hero_battlefield if creature.attack_declared)

    def select_attackers(self, attackers):
        # Convert to list of cards
        if not isinstance(attackers, list):
            attackers = [attackers]
        if all(isinstance(grp_id, int) for grp_id in attackers):
            attackers = list(minion for minion in self.game.offensive_army if minion.grp_id in attackers)
        # Check if the requested attackers are correct
        attackers = list(minion for minion in attackers if minion.attack_ready)

        # Cancel attack if got an empty list
        if not attackers:
            while game_dict.declare_attackers_phase:
                self.cancel()
                time.sleep(1)
            return
        # Use space if all attack
        if game_dict.declare_attackers_phase and len(attackers) == len(game_dict.offensive_army):
            if len(self.attack_declared_creatures) == 0:
                self.space()
                time.sleep(1)
                self.attack_villain()   # if planeswalker: select villain as objective

        # Select loop
        while game_dict.declare_attackers_phase and not self.check_declared_attackers(attackers):
            # Unselect wrong attacked
            if wrong_attack := list(minion for minion in self.attack_declared_creatures if minion not in attackers):
                for _ in self.move_to_creatures(wrong_attack):
                    if self.game.cursor in wrong_attack and self.game.cursor.attack_declared:
                        self.click()
                        time.sleep(0.6)
            # Select attackers
            for _ in self.move_to_creatures(attackers):
                if self.game.cursor in attackers and not self.game.cursor.attack_declared:
                    self.click()
                    time.sleep(0.6)
                    if self.check_declared_attackers(attackers):
                        break
            self.attack_villain()   # if planeswalker: select villain as objective
        self.space()

    def attack_villain(self):
        if any(permanent.is_planeswalker for permanent in game_dict.villain_battlefield):
            self.move_to(*self.coord.villain)
            time.sleep(0.2)
            self.click()
            time.sleep(0.4)

    def attack_if_kill(self):
        villain_army = game_dict.villain_defensive_army
        max_enemy_toughness = max((minion.toughness for minion in villain_army), default=0)
        max_flying_enemy_toughness = max((minion.toughness for minion in villain_army if minion.fly), default=0)
        first_damage_enemies = list(minion for minion in villain_army if minion.first_strike or minion.double_strike)
        max_enemy_first_damage = max((minion.power for minion in first_damage_enemies), default=0)
        max_enemy_flying_first_damage = max((minion.power for minion in first_damage_enemies if minion.fly), default=0)

        attackers = list(minion for minion in game_dict.offensive_army if minion.power >= max_enemy_toughness)
        attackers = list(minion for minion in attackers if minion.toughness > max_enemy_first_damage)
        own_flyers = list(minion for minion in game_dict.offensive_army if minion.fly)
        flying_attackers = list(flyer for flyer in own_flyers if flyer.power >= max_flying_enemy_toughness)
        flying_attackers = list(flyer for flyer in flying_attackers if flyer.toughness > max_enemy_flying_first_damage)
        attackers.extend(minion for minion in flying_attackers if minion not in attackers)

        self.select_attackers(attackers)

    def attack_with_all(self):
        self.select_attackers(game_dict.offensive_army)
