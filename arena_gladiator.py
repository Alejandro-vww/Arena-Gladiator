import time

from aplication_status import AplicationStatus
from game_dict import GameDict
from game_window.executor import Executor
from zone_27 import Zone27

from minion_of_the_mighty import MinionOfTheMighty
from default_mode import DefaultMode


class ArenaGladiator:
    def __init__(self, custom_mode = None):
        self.game_dict = GameDict()
        self.app_status = AplicationStatus()
        self.execute = Executor()

        self.mode = custom_mode
        self.default_mode = DefaultMode
        self.advance_to = None
        self.phases = ["Phase_Beginning", "Phase_Main1", "Phase_Combat", "Phase_Main2", "Phase_Ending"]

    def play(self):
        print('entrando')
        # MULLIGAN
        while self.app_status.mulligan:
            self.game_dict.wait()
            self.select_custom_or_default_play('mulligan')


        # GAME
        while self.app_status.screen == 'Playing':
            print('nuevo ciclo')
            self.game_dict.wait()

            # ZONE 27
            if self.game_dict.instances.stack:
                Zone27.solve(self.game_dict.instances.stack)

            # HERO TURN
            if self.game_dict.hero_turn:

                if self.game_dict.phase == 'Phase_Beginning':
                    self.execute.space()
                    time.sleep(1)

                elif self.game_dict.phase == 'Phase_Main1':
                    if self.game_dict.can_play_land:
                        self.select_custom_or_default_play('play_land')
                    else:
                        self.select_custom_or_default_play('main_phase_1')

                elif self.game_dict.phase == 'Phase_Combat':
                    if self.game_dict.declare_attackers_phase:
                        self.select_custom_or_default_play('declare_attackers')
                    else:
                        self.execute.space()

                elif self.game_dict.phase == 'Phase_Main2':     #'Phase_Ending'?
                    self.select_custom_or_default_play('main_phase_2')

                else:
                    print('espacio genérico en tu turno')

            # TURNO OPONENTE

            elif self.game_dict.phase == 'Phase_Combat' and self.game_dict.step == 'Step_DeclareBlock':
                self.execute.space()

            else:
                print('espacio genérico')
                self.execute.space()

            if not self.game_dict.active and not self.game_dict.hero_turn:
                print('scan')
                self.execute.scan_hand()

        while self.app_status.screen == 'Confused':
            self.execute.concede()
            time.sleep(2)

    def select_custom_or_default_play(self, phase_name):
        # Execute custom/default play_phase_function and then advance to the phase returned by that function
        if hasattr(self.mode, phase_name):
            exec(f'self.advance_to_phase(self.mode.{phase_name}())')
        else:
            exec(f'self.advance_to_phase(self.default_mode.{phase_name}())')

    def advance_to_phase(self, phase):
        if phase not in self.phases:
            return False
        self.game_dict.wait()
        if self.game_dict.hero_turn and self.phases.index(phase) > self.phases.index(self.game_dict.phase):
            self.execute.space()
            time.sleep(0.2)


