from aplication_status import AplicationStatus
from game_dict import GameDict
from game_window.executor import Executor
from instances.card import Card


game_dict = GameDict()
app_status = AplicationStatus()
execute = Executor()

class MinionOfTheMighty:

    @staticmethod
    def mulligan():
        hand = list(game_dict.instances.hand)
        Catalizadores = catalizadores(hand)
        Mana = tierras_dual_mono(hand)
        Descartar = []
        if minion not in hand or not any_dragon(hand):
            execute.mulligan() if game_dict.mulligan_count < 4 else execute.concede()

        if game_dict.mulligan_count == 0:
            if max_buff() == 0 or sum(Mana) == 0 or sum(Mana) == 1 and max_buff() < 6:  # Descarta si no tienes Messi, dragón, tierras o te falta 1 tierra y 1 catalizador
                execute.mulligan()
            elif sum(Mana) == 1 and not maximizar(hand) and Catalizadores[1] == 0 and Mana[0] == 0:  # Descarta si solo tienes una tierra monocolor y ningún catalizador rojo ni maximizar
                execute.mulligan()
            else:
                execute.space()

        elif game_dict.mulligan_count == 1:
            if sum(Catalizadores) == 0 or sum(Mana) == 0 or sum(Mana) == 1 and Catalizadores[0] == 0 and sum(Catalizadores[
                                                  0:3]) < 2:  # Descarta si no tienes Messi, dragón, tierras o te falta 1 tierra y 1 catalizador
                return 'Mulligan'
            elif sum(Mana) == 1:
                if Catalizadores[0] == 0 and Catalizadores[1] == 0 and Mana[
                    0] == 0:  # Descarta si solo tienes una tierra monocolor y ningún catalizador rojo ni maximizar
                    return 'Mulligan'
            if maximizar(hand):
                if Mana[0] - Mana[2] > 0 and sum(Mana[
                                                 0:2]) > 1:  # Comprueba que haya más de 1 tierra y que tengamos una dual no tempo para descartar el resto
                    Descartar.append(ordenar_tierras(hand)[0])
                elif sum(Mana[0:2]) > 2:  # Si hay 3 o más tierras
                    Descartar.append(ordenar_tierras(hand)[0])
                elif Mana[2] > 1:  # Si hay más de un templo que entra girado
                    Descartar.append(ordenar_tierras(hand)[0])
                elif sum(Catalizadores) > 1:
                    Descartar.append(ordenar_hechizos(hand)[0])
                elif contar_dragones(hand) > 1:
                    Descartar.append(ordenar_dragones(hand)[0])
                elif hand.count(
                        77261) > 2:  # 2 tierras, maximizar y 1 dragón = 4, deben haber 3 messis o algo ha ido mal
                    Descartar.append(77261)
                else:
                    print('fallo muligan con maximizar 1 a descartar')
            else:  # Si no hay maximizar
                if sum(Mana[0:2]) > 3:  # 4 o más tierras descartas una sí o sí
                    Descartar.append(ordenar_tierras(hand)[0])
                elif sum(Mana[0:2]) > 2:  # Si hay 3 o más tierras
                    if catalizadores(hand)[
                        1] > 0:  # Si tenemos un hechizo rojo no habría problema con tierras monocolor
                        Descartar.append(ordenar_tierras(hand)[0])
                    elif Mana[1] == 3 and catalizadores(hand)[
                        2] > 1:  # Único caso en el que nos quedaríamos 3 tierras es si las 3 son monocolor y tenemos uno o más hechizos verdes, descartaríamos el segundo hechizo verde en espera de que nos caiga el segundo rojo y tendríamos tierra en caso de caiga el segundo verde
                        Descartar.append(ordenar_hechizos(hand)[0])
                    elif Mana[0] - Mana[2] > 0 or Mana[
                        2] > 1:  # Si hay una dual no tempo o más de 1 dual tempo descartaríamos tierra tempo primero
                        Descartar.append(ordenar_tierras(hand)[0])
                    else:
                        Descartar.append(ordenar_tierras(hand, dual=True)[
                                             0])  # Falta el caso 2 mono 1 dual 2 hechizos verdes, descartas 1 verde esperando que caiga un rojo y si no pos adivinas con la tempo
                elif sum(Catalizadores) > 2:
                    Descartar.append(ordenar_hechizos(hand)[0])
                elif contar_dragones(hand) > 1:
                    Descartar.append(ordenar_dragones(hand)[0])
                elif hand.count(
                        77261) > 1:  # 3 tierras, 1 hechizo y 1 dragón o 2t 2h 1d = 5, deben haber 2 messis o algo ha ido mal
                    Descartar.append(77261)
                else:
                    print('fallo muligan sin maximizar 1 a descartar')
            return Descartar

        elif game_dict.mulligan_count == 2:
            if not messi(hand) or not any_dragon(hand) or sum(Catalizadores) == 0 or sum(
                    Mana) == 0:  # Descarta si no tienes Messi, dragón, tierras o hechizos
                return 'Mulligan'
            Descartar = hand.copy()
            if maximizar(hand):
                Descartar.remove(77261)
                Descartar.remove(ordenar_dragones(hand)[-1])
                Descartar.remove(ordenar_hechizos(hand)[-1])
                Descartar.remove(ordenar_tierras(hand)[-1])
                if Mana[0] - Mana[2] == 0 and sum(
                        tierras_dual_mono(Descartar)) > 0:  # Si no hay tierra doble que entre enderezada
                    Descartar.remove(ordenar_tierras(Descartar)[-1])
                else:
                    if 77261 in Descartar:
                        Descartar.remove(77261)
                    elif contar_dragones(Descartar) > 0:
                        Descartar.remove(ordenar_dragones(Descartar)[-1])
                    elif sum(catalizadores(Descartar)) > 0:
                        Descartar.remove(ordenar_hechizos(Descartar)[-1])
                    else:
                        Descartar.remove(ordenar_tierras(Descartar, dual=True)[-1])
            else:
                Descartar.remove(77261)
                Descartar.remove(ordenar_dragones(hand)[-1])
                Descartar.remove(ordenar_hechizos(hand)[-1])
                if Catalizadores[1] > 0:
                    Descartar.remove(ordenar_tierras(hand)[-1])
                else:
                    Descartar.remove(ordenar_tierras(hand, dual=True)[-1])
                if sum(tierras_dual_mono(Descartar)) > 0:
                    Descartar.remove(ordenar_tierras(Descartar)[-1])
                elif sum(catalizadores(Descartar)) > 0:
                    Descartar.remove(ordenar_hechizos(Descartar)[-1])
                elif 77261 in Descartar:
                    Descartar.remove(77261)
                else:
                    Descartar.remove(ordenar_dragones(Descartar)[-1])
            return Descartar

        elif game_dict.mulligan_count == 3:
            if not messi(hand) or not any_dragon(hand) or sum(Catalizadores) == 0 and sum(Mana) < 2 or sum(
                    Mana) == 0:  # Mínimo debes tener messi, dragón y (1 tierra 1 catalizador / 2 tierras)
                return 'Mulligan'
            Descartar = hand.copy()
            if maximizar(hand):
                Descartar.remove(77261)
                Descartar.remove(ordenar_dragones(hand)[-1])
                Descartar.remove(ordenar_hechizos(hand)[-1])
                Descartar.remove(ordenar_tierras(hand, dual=True)[-1])
            else:
                Descartar.remove(77261)
                Descartar.remove(ordenar_dragones(hand)[-1])
                Descartar.remove(ordenar_tierras(hand, dual=True)[-1])

                if sum(Catalizadores) > 0:  # Nos quedamos con el hechizo o la segunda tierra
                    Descartar.remove(ordenar_hechizos(hand)[-1])
                else:
                    Descartar.remove(ordenar_tierras(Descartar, dual=True)[-1])

            return Descartar

        elif game_dict.mulligan_count == 4:
            Descartar = hand.copy()
            if maximizar(hand) and messi(hand) and any_dragon(hand):
                Descartar.remove(77261)
                Descartar.remove(ordenar_dragones(hand)[-1])
                Descartar.remove(ordenar_hechizos(hand)[-1])  # Será maximizar o algo falla
                return Descartar
            else:
                return 'Concede'

    @staticmethod
    def play_land():
        if any(dual_land in game_dict.instances.hand for dual_land in [69407, 82302, 83949]):
            Oliva.play_card([69407, 82302, 83949])
        elif Oliva.mesa.tierrasBajadas == 0:
            Oliva.play_card([73476, 77365, 70755], 'rojo')
        elif Oliva.mesa.tierrasBajadas == 1:
            if spells[0] > 0 or spells[2] >= 2 or spells[1] > 0 and spells[
                2] > 0:  # Con combo algún hechizo verde en mano baja verde, mínimo un rojo se debe tener a esta altura
                Oliva.play_card([73476, 77365, 70755], 'verde')
                # continue
            elif spells[1] >= 2:
                Oliva.play_card([73476, 77365, 70755], 'rojo')
                # continue
            elif 70755 in game_dict.instances.hand:
                Oliva.play_card(70755)
                # continue
            else:
                print('no tierra')
                Oliva.space()
                time.sleep(0.4)
        elif Oliva.mesa.tierrasBajadas == 2 and max(opt[0] for opt in comb_mana) == max(
                opt[1] for opt in comb_mana) == 1:  # 1 roja y 1 verde
            if spells[1] >= 2:
                Oliva.play_card([73476, 77365, 70755], 'rojo')
                # continue
            elif spells[0] > 0 or spells[2] >= 2:
                Oliva.play_card([73476, 77365, 70755], 'verde')
                # continue
            elif spells[1] >= 1 and spells[2] >= 1:
                Oliva.play_card([73476, 77365, 70755], 'verde')
                # continue
            elif 70755 in game_dict.instances.hand:
                Oliva.play_card(70755)
                # continue
            else:
                print('no tierra')
        else:
            if max(opt[0] for opt in comb_mana) <= max(opt[1] for opt in comb_mana):
                Oliva.play_card([73476, 77365, 70755], 'rojo')
                # continue
            else:
                Oliva.play_card([73476, 77365, 70755], 'verde')
                # continue

    @staticmethod
    def main_phase_1():
        if combo_breaker(Oliva.mesa):
            print('tenemos combo')
            if sum(crtr.power for crtr in Oliva.mesa.campoBatalla if crtr.attack_ready) >= 6:
                print('avanzamos a combate')
                Oliva.space()
            else:
                for criatura in Oliva.mesa.campoBatalla:
                    if criatura == 77261 and criatura.attack_ready:
                        instMessi = criatura.instance_id
                if spells[0] > 0 and max(comb[1] for comb in comb_mana) > 0:
                    Oliva.play_card(71520, instMessi)
                elif spells[1] > 0 and max(comb[0] for comb in comb_mana) > 0:
                    Oliva.play_card([71485, 77520, 54613], instMessi)
                elif spells[2] > 0 and max(comb[1] for comb in comb_mana) > 0:
                    Oliva.play_card([69613, 77317], instMessi)
                time.sleep(1.5)

        # else:
            print('no tenemos combo')
            Oliva.play_card(77261) if 77261 in game_dict.instances.hand else None
            print('avanzamos a combate')
            Oliva.space()

    @staticmethod
    def declare_attackers():
        if sum(criatura.power for criatura in Oliva.mesa.campoBatalla if
               criatura.attack_ready) >= 5:
            Oliva.space()
            if Oliva.mesa.planeswalkersVillain:
                Oliva.movimiento_corregido(965, 120)
                time.sleep(0.1)
                Oliva.click()
        else:
            Oliva.rechazar()
            time.sleep(0.5)
            Oliva.rechazar()

    @staticmethod
    def main_phase_2():
        Oliva.play_card(77261) if 77261 in Oliva.mesa.mano else None
        if Oliva.mesa.manaConTesoros > 6 and contar_dragones(Oliva.mesa.mano) > 0:
            dragones = ordenar_dragones(Oliva.mesa.mano)
            for dragon in dragones:
                if dragon in Oliva.mesa.campoBatalla and dragon in [70792, 77302, 68653]:
                    dragones.remove(dragon)
            Oliva.play_card(dragones)
        Oliva.space()

    @staticmethod
    def dragon_value(card: Card):
        if card == 70792:   #Monte venus
            return 110
        if card == 81664:
            return 109
        return card.mana_cost

minion = 77261
dual_lands = [69407, 82302, 83949]



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

def max_buff():
    buff_spells = catalizadores(game_dict.instances.hand)
    return buff_spells[0] * 6 + sum(buff_spells[1:3]) * 3

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

def combo_breaker(mesa):
    print('Tendremos combo?')
    print(any(criatura == 77261 and criatura.attack_ready for criatura in mesa.campoBatalla))
    if not any(criatura == 77261 and criatura.attack_ready for criatura in mesa.campoBatalla):
        print(f'campo batalla {list(criatura.dictionary for criatura in mesa.campoBatalla)}')
    print(any_dragon(game_dict.instances.hand))
    if any(criatura == 77261 and criatura.attack_ready for criatura in mesa.campoBatalla) and any_dragon(
            game_dict.instances.hand):
        spells = catalizadores(game_dict.instances.hand)
        mana = mesa.mana
        print(f'Fuersa total: {sum(crtr.power for crtr in mesa.campoBatalla if crtr.attack_ready)}')
        if sum(crtr.power for crtr in mesa.campoBatalla if crtr.attack_ready) >= 6:
            return True

        elif sum(crtr.power for crtr in mesa.campoBatalla if crtr.attack_ready) >= 3:
            if spells[0] > 0 and max(comb[1] for comb in mana) > 0:
                return True
            if spells[1] > 0 and max(comb[0] for comb in mana) > 0:
                return True
            if spells[2] > 0 and max(comb[1] for comb in mana) > 0:
                return True
            return False

        elif sum(crtr.power for crtr in mesa.campoBatalla if crtr.attack_ready) >= 0:
            if spells[0] > 0 and max(comb[1] for comb in mana) > 0:
                return True
            if spells[1] >= 2 and max(comb[0] for comb in mana) >= 2:
                return True
            if spells[2] >= 2 and max(comb[1] for comb in mana) >= 2:
                return True
            if spells[1] > 0 and spells[2] > 0 and max(comb[0] for comb in mana) > 0 and max(
                    comb[1] for comb in mana) > 0 and mesa.tierras_enderezadas >= 2:
                return True
            return False


