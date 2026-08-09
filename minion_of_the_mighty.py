import time

from game.aplication_status import AplicationStatus
from game.game import GameDict
from game.controller.executor import Executor
from game.game_objects.cards.card import Card
from data_base.names_database import *

game_dict = GameDict()
app_status = AplicationStatus()
execute = Executor()


class MinionOfTheMighty:

    @staticmethod
    def mulligan():
        while game_dict.status.mulligan:
            game_dict.wait_action()
            hand = game_dict.hand
            mull_count = game_dict.mulligan_count

            # Concede if mulligan = 4 and no scale up with minion and dragon
            if mull_count == 4:
                execute.concede() if scale_up not in hand or not minion_with_dragon() else execute.space()
                print('1')
                break
            # Discard if hand with no minion, no dragon or no land
            elif not minion_dragon_land():
                execute.mulligan()
                print('2')
            # Discard if mull count <= 1 and 2 or more card are needed
            elif mull_count <= 1 and cards_needed() >= 2:
                execute.mulligan()
                print('3')
            # Discard if 3 or more cards are needed
            elif cards_needed() >= 3:
                execute.mulligan()
                print('4')
            else:
                print('5')
                execute.space()
                break

        time.sleep(1)
        if not game_dict.status.screen == 'Playing':
            return False

        cards_to_keep = []
        cards_to_discard = game_dict.hand
        number_of_discards = game_dict.mulligan_count

        # Popping the cards to keep from the hand (hand = cards_to_discard)
        pop_one_minion(cards_to_keep, cards_to_discard)
        pop_one_dragon(cards_to_keep, cards_to_discard)

        for _ in range(1):
            # Minion, dragon + 1 Spell
            pop_one_spell(cards_to_keep, cards_to_discard)
            if len(cards_to_discard) == number_of_discards:
                break

            # Minion, dragon, spell + 2 land
            pop_one_land(cards_to_keep, cards_to_discard)
            if len(cards_to_discard) == number_of_discards:
                break
            pop_one_land(cards_to_keep, cards_to_discard)
            if len(cards_to_discard) == number_of_discards:
                break

            # Minion, dragon, spell, 2 lands + 1 spell
            pop_one_spell(cards_to_keep, cards_to_discard)
            if len(cards_to_discard) == number_of_discards:
                break

            # Minion, dragon, 2 spells, 2 lands + 1 land
            pop_one_land(cards_to_keep, cards_to_discard)
            if len(cards_to_discard) == number_of_discards:
                break

            # Minion, dragon, 2 spells, 3 lands + 1 spell
            pop_one_spell(cards_to_keep, cards_to_discard)
            if len(cards_to_discard) == number_of_discards:
                break
            # + 1 minion + 1 dragon
            pop_one_minion(cards_to_keep, cards_to_discard)
            if len(cards_to_discard) == number_of_discards:
                break
            pop_one_dragon(cards_to_keep, cards_to_discard)
            if len(cards_to_discard) == number_of_discards:
                break
            # + whatever
            for _ in range(cards_to_discard - number_of_discards):
                cards_to_keep.append(cards_to_discard.pop(0))

        execute.mulligan_discard(cards_to_discard)

    @staticmethod
    def play_land():
        print('land')
        total_lands_on_field = len(list(card for card in game_dict.hero_battlefield if card.is_land))
        lands_in_hand = sorted(list(card for card in game_dict.hand if card.is_land), key=land_value, reverse=True)
        buff_spells = buffing_spells_vector()

        if total_lands_on_field == 0:
            execute.play_custom_color_land(lands_in_hand[0], 'red')
        elif buff_spells[0] + buff_spells[2] >= 1:
            execute.play_custom_color_land(lands_in_hand[0], 'green')
        elif buff_spells[1] >= 2:
            execute.play_custom_color_land(lands_in_hand[0], 'red')
        elif dual := list(card for card in lands_in_hand if card in all_dual_lands):
            execute.play_cards(dual[0])
        elif total_lands_on_field + len(lands_in_hand) >= 4:
            # So you never end up with all lands in one color
            if total_lands_on_field % 2 == 0:
                execute.play_custom_color_land(lands_in_hand[0], 'red')
            else:
                execute.play_custom_color_land(lands_in_hand[0], 'green')
        time.sleep(1)
        game_dict.wait_action()
        MinionOfTheMighty.main_phase_1()

    @staticmethod
    def main_phase_1():
        print('main')
        if combo_breaker():
            print('tenemos combo')
            if sum(creature.power for creature in game_dict.offensive_army) < 6:
                max_mana = game_dict.max_mana_vector
                minion_instance = list(creature for creature in game_dict.offensive_army if creature == minion)[0]
                red_spells_in_hand = list(card for card in game_dict.hand if card in red_spells)
                green_spells_in_hand = list(card for card in game_dict.hand if card in green_spells_plus_3)
                if scale_up in game_dict.hand and max_mana[1] > 0:
                    execute.cast_on(scale_up, minion_instance, option='left')
                elif red_spells_in_hand and max_mana[0] > 0:
                    execute.cast_on(red_spells_in_hand[0], minion_instance)
                elif green_spells_in_hand and max_mana[1] > 0:
                    execute.cast_on(green_spells_in_hand[0], minion_instance)
                time.sleep(1.5)
            else:
                return 'Phase_Combat'
        elif minion in game_dict.hand and game_dict.max_mana_vector[0]:
            execute.play_cards(minion)
        else:
            return 'Phase_Combat'

    @staticmethod
    def declare_attackers():
        print('atack')
        if sum(creature.power for creature in game_dict.offensive_army) >= 6:
            execute.attack_with_all()
        else:
            execute.cancel()

    @staticmethod
    def main_phase_2():
        print('main 2')
        execute.play_optimized_creatures(use_treasures=True)
        return 'End_Turn'


def dragons(hand=None):
    if not hand:
        hand = game_dict.hand
    return list(card for card in hand if card.is_dragon)


def minion_with_dragon(hand=None):
    if not hand:
        hand = game_dict.hand
    return minion in hand and dragons(hand=hand)


def minion_dragon_land(hand=None):
    if not hand:
        hand = game_dict.hand
    return minion_with_dragon(hand=hand) and list(card for card in hand if card.is_land)


def dragon_value(card: Card):
    if card == 70792:   # Monte venus
        return 110
    if card == 81664:   # Oro anciano
        return 109
    return card.mana_cost if card.is_dragon else 0


def buffing_spells_vector():
    hand = game_dict.hand
    # [Scale up, red, green, wild form (extra copies)]
    buff_spells = [0, 0, 0, 0]
    wild_form_counted = False
    for card in hand:
        if card == scale_up:
            buff_spells[0] += 1
        elif card in red_spells:
            buff_spells[1] += 1
        elif card == giant_growth:
            buff_spells[2] += 1
        elif card == wild_form and not wild_form_counted:
            buff_spells[2] += 1
            wild_form_counted = True
        elif card == wild_form:
            buff_spells[3] += 1
    return buff_spells


def max_buff():
    buff_spells = buffing_spells_vector()
    return buff_spells[0] * 6 + sum(buff_spells[1:3]) * 3


def mana_for_buffs():   # [red, green, spells to be drawn]
    hand = game_dict.hand
    if scale_up in hand:
        return [0, 1, 0]
    buff_spells = buffing_spells_vector()
    red = min(buff_spells[1], 2)        # You don´t need more than 2
    green = min(buff_spells[2], 2)
    return [red, green - red, max(2 - red - green, 0)]  # Again, you don't need more than 2


def cards_needed() -> int:       # Spells + lands (+0.5 if spell and land don't match)
    hand = game_dict.hand
    hand_dual_lands = len(list(card for card in hand if card in all_dual_lands))
    hand_mono_dual_lands = len(list(card for card in hand if card in mono_dual_lands))
    total_lands = hand_dual_lands + hand_mono_dual_lands
    mana_needed = mana_for_buffs()
    # Scale up otherwise you should need at least 2 mana
    if sum(mana_needed) == 1:
        return 0 if hand_dual_lands >= 1 or total_lands >= 2 else 1
    # 2 green spells
    elif mana_needed[1] == 2:
        if hand_dual_lands >= 1:
            return max(2 - total_lands, 0)
        else:
            return max(3 - total_lands, 0)
    # 2 spells (at least 1 should be red)
    elif sum(mana_needed[:2]) == 2:
        return max(2 - total_lands, 0)
    # 1 red spell
    elif mana_needed[0] == 1:
        return max(2 - total_lands, 0) + 1
    # 1 green spell
    elif mana_needed[1] == 1:
        if hand_dual_lands >= 1:
            return max(2 - total_lands, 0) + 1
        else:
            return max(2.5 - total_lands, 0) + 1
    # 0 spells
    return max(2 - total_lands, 0) + 2


def land_value(card):
    if card in dual_fast_lands:
        return 10
    elif card in dual_slow_lands:
        return 5
    elif card in mono_dual_lands:
        return 1
    return 0


def spell_value(card):
    if card == scale_up:
        return 10
    elif card == titan_strength:
        return 5
    elif card in red_spells:
        return 3
    elif card in green_spells:
        return 1
    return 0


def pop_one_minion(keep_list, discard_list):
    if minion in discard_list:
        index = discard_list.index(minion)
        keep_list.append(discard_list.pop(index))


def pop_one_dragon(keep_list, discard_list):
    if dragons_list := sorted(dragons(hand=discard_list), key=dragon_value, reverse=True):
        index = discard_list.index(dragons_list[0])
        keep_list.append(discard_list.pop(index))


def pop_one_spell(keep_list, discard_list):
    if spell_list := list(card for card in discard_list if card in red_spells + green_spells):
        spell_list.sort(key=spell_value, reverse=True)
        index = discard_list.index(spell_list[0])
        keep_list.append(discard_list.pop(index))


def pop_one_land(keep_list, discard_list):
    if land_list := list(card for card in discard_list):
        land_list.sort(key=land_value, reverse=True)
        index = discard_list.index(land_list[0])
        keep_list.append(discard_list.pop(index))


def combo_breaker():
    offensive_power = sum(creature.power for creature in game_dict.offensive_army)
    if minion in game_dict.offensive_army and dragons() and max_buff() + offensive_power >= 6:
        if offensive_power >= 6:
            return True

        mana_needed = mana_for_buffs()
        mana = game_dict.max_mana_vector
        buff_spells = buffing_spells_vector()
        # This prioritizes red spells, so you can lack a red land with 2 red + green spells and red, green lands
        if min(mana[0] - mana_needed[0], mana[1] - mana_needed[1]) >= 0:
            return True
        # This check one red one green
        if buff_spells[1] >= 1 and mana[0] >= 1 and buff_spells[2] >= 1 and mana[1] >= 1:
            return True
        # This check red or green spell + land
        if offensive_power >= 3:
            if buff_spells[1] >= 1 and mana[0] >= 1 or buff_spells[2] >= 1 and mana[1] >= 1:
                return True
        return False








# El irremplazable

def messi(mano):
    return True if 77261 in mano else False

# Ataques rojos

def carga_temeraria(mano):
    return True if 71485 in mano else False

def enfurecer(mano):
    return True if 77520 in mano else False

def fuerza_titanica(mano):
    return True if 54613 in mano else False

# Ataques verdes

def maximizar(mano):
    return True if 71520 in mano else False

def crecimiento_gigante(mano):
    return True if 69613 in mano else False

def forma_salvaje(mano):
    return True if 77317 in mano else False

# Tierras

def mountain(mano):
    return True if 79095 in mano else False

def bosque(mano):
    return True if 79096 in mano else False

def senda_de_cumbrerriscos(mano):
    return True if 73476 in mano else False

def terreno_aplastador(mano):
    return True if 69407 in mano else False

def foresta_karplusana(mano):
    return True if 82302 in mano else False

def templo_del_abandono(mano):
    return True if 70755 in mano else False

def planta_de_eter_central(mano):
    return True if 75857 in mano else False

def templo_de_la_reina_de_los_dragones(mano):
    return True if 77365 in mano else False

def any_dragon(mano):
    return True if any(carta.is_dragon for carta in mano) else False

def catalizadores(mano):
    catalizadores = [0, 0, 0,
                     0]  # Maximizar, hechizos rojos, hechizos verdes, formas salvaje extras (la primera cuenta en hechizo verde)
    formaContada = False
    for carta in mano:
        if maximizar(carta):
            catalizadores[0] += 1
        elif carga_temeraria(carta) or enfurecer(carta) or fuerza_titanica(carta):
            catalizadores[1] += 1
        elif crecimiento_gigante(carta):
            catalizadores[2] += 1
        elif forma_salvaje(carta) and not formaContada:
            catalizadores[2] += 1
            formaContada = True
        elif forma_salvaje(carta) and formaContada:
            catalizadores[3] += 1
    return catalizadores

# Devuelve [nº tierras duales, nº mono, nº entran giradas] (el templo suma a dual y a girada)
def tierras_dual_mono(mano):
    recuento = []
    for tierra in mano:
        if tierra == 73476:  # Senda
            recuento.append('mono')
        elif tierra == 77365:  # templo dragones
            recuento.append('mono')
        elif tierra == 69407:  # aplastador
            recuento.append('dual')
        elif tierra == 83949:  # Copperline
            recuento.append('dual')
        elif tierra == 82302:  # karplusana
            recuento.append('dual')
        elif tierra == 70755:  # templo
            recuento.append('dual')
            recuento.append('tempo')
    return recuento.count('dual'), recuento.count('mono'), recuento.count('tempo')

def contar_dragones(mano):
    return len(list(carta for carta in mano if carta.is_dragon))

# Devuelve lista de grpId ordenados de menor a valor de las tierras, si dual == True templo del abandono tendrá prioridad sobre las monocolor
def ordenar_tierras(mano, dual=False):
    if dual:
        orden = [77365, 73476, 70755, 82302, 69407, 83949]
    else:
        orden = [70755, 77365, 73476, 82302, 69407, 83949]
    Mano = filter(lambda x: x in orden, mano)
    return sorted(Mano, key=lambda carta: orden.index(carta))

# Ordena los hechizos por valor de menor a mayor (más valiosos los rojos para simplificar situaciones)
def ordenar_hechizos(mano):
    orden = [77317, 69613, 71485, 77520, 54613, 71520]
    Mano = filter(lambda x: x in orden, mano)
    return sorted(Mano, key=lambda carta: orden.index(carta))

# De menor a mayor valor
def ordenar_dragones(mano):
    orden = [68653, 77302, 81664, 70792]
    orden.extend(carta for carta in mano if carta.is_dragon)
    Mano = filter(lambda x: x in orden, mano)
    return sorted(Mano, key=lambda carta: orden.index(carta))
    # falta bajar en prioridad los legendarios repetidos

