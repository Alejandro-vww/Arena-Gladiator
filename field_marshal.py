import time

from game_dict import GameDict

game_dict = GameDict()


class FieldMarshal:
    coord = None
    game_dict = None

    def move_to(self, x, y):
        raise NotImplementedError("This method must be implemented by the subclass.")

    def space(self):
        raise NotImplementedError("This method must be implemented by the subclass.")

    def click(self):
        raise NotImplementedError("This method must be implemented by the subclass.")

    def cancel(self):
        raise NotImplementedError("This method must be implemented by the subclass.")

    def check_declared_attackers(self, attack_command):
        sorted_attack_command = sorted(attack_command, key=lambda instance: instance.instance_id)
        sorted_attackers = sorted(self.attack_declared_creatures(), key=lambda instance: instance.instance_id)
        return sorted_attack_command == sorted_attackers

    def attack_declared_creatures(self):
        return list(creature for creature in game_dict.instances.hero_battlefield if creature.attack_declared)

    def move_to_creatures(self, card_list):
        if not isinstance(card_list, list):
            card_list = [card_list]
        instance_ids = list(card.instance_id for card in card_list)

        for x in range(1701, 200, -50):
            self.move_to(self.coord.scale_x_1080p(x), self.coord.scale_y_1080p(590))
            time.sleep(0.4)
            instance_id = self.game_dict.cursor.instance_id if self.game_dict.cursor else None
            if self.game_dict.cursor and instance_id in instance_ids:
                instance_ids.remove(instance_id)
                yield

            if not instance_ids:
                break

    def select_attackers(self, attackers):
        # Convert to list of cards
        if not isinstance(attackers, list):
            attackers = [attackers]
        if all(isinstance(grp_id, int) for grp_id in attackers):
            attackers = list(minion for minion in self.game_dict.instances.offensive_army if minion.grp_id in attackers)
        # Check if the requested attackers are correct
        attackers = list(minion for minion in attackers if minion.attack_ready)
        # Cancel attack if got an empty list
        if not attackers:
            while game_dict.declare_attackers_phase:
                self.cancel()
                time.sleep(1)
            return
        # Use space if all attack
        if game_dict.declare_attackers_phase and len(attackers) == len(game_dict.instances.offensive_army):
            if len(self.attack_declared_creatures()) == 0:
                self.space()
                time.sleep(0.6)
                self.attack_villain()   # if planeswalker: select villain as objective
        # Select loop
        while game_dict.declare_attackers_phase and not self.check_declared_attackers(attackers):
            # Unselect wrong attacked
            if wrong_attack := list(minion for minion in self.attack_declared_creatures() if minion not in attackers):
                for _ in self.move_to_creatures(wrong_attack):
                    if self.game_dict.cursor in wrong_attack and self.game_dict.cursor.attack_declared:
                        self.click()
                        time.sleep(0.6)
            # Select attackers
            for _ in self.move_to_creatures(attackers):
                if self.game_dict.cursor in attackers and not self.game_dict.cursor.attack_declared:
                    self.click()
                    time.sleep(0.6)
                    if self.check_declared_attackers(attackers):
                        break
            self.attack_villain()   # if planeswalker: select villain as objective
        self.space()

    def attack_villain(self):
        if any(permanent.is_planeswalker for permanent in game_dict.instances.villain_battlefield):
            self.move_to(*self.coord.villain)
            time.sleep(0.2)
            self.click()
            time.sleep(0.4)

    def attack_if_kill(self):
        villain_army = game_dict.instances.villain_defensive_army
        max_enemy_toughness = max((minion.toughness for minion in villain_army), default=0)
        max_flying_enemy_toughness = max((minion.toughness for minion in villain_army if minion.fly), default=0)
        first_damage_enemies = list(minion for minion in villain_army if minion.first_strike or minion.double_strike)
        max_enemy_first_damage = max((minion.power for minion in first_damage_enemies), default=0)
        max_enemy_flying_first_damage = max((minion.power for minion in first_damage_enemies if minion.fly), default=0)

        attackers = list(minion for minion in game_dict.instances.offensive_army if minion.power >= max_enemy_toughness)
        attackers = list(minion for minion in attackers if minion.toughness > max_enemy_first_damage)
        own_flyers = list(minion for minion in game_dict.instances.offensive_army if minion.fly)
        flying_attackers = list(minion for minion in own_flyers if minion.power >= max_flying_enemy_toughness)
        flying_attackers = list(minion for minion in flying_attackers if minion.toughness > max_enemy_flying_first_damage)
        attackers.extend(minion for minion in flying_attackers if minion not in attackers)

        self.select_attackers(attackers)