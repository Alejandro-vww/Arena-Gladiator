import time

from game.application_status import ApplicationStatus
from game.game import GameDict
from game.controller.executor import Executor
from zone_27 import Zone27

from default_mode import DefaultMode


class ArenaGladiator:
    def __init__(self, custom_mode=None):
        self.game_dict = GameDict()
        self.app_status = ApplicationStatus()
        self.execute = Executor()

        self.mode = custom_mode
        self.default_mode = DefaultMode
        self.advance_to = None
        self.phases = ["Phase_Beginning", "Phase_Main1", "Phase_Combat", "Phase_Main2", "Phase_Ending", "End_Turn"]

    def play(self):
        # MULLIGAN
        while self.app_status.mulligan:
            self.game_dict.wait_action()
            self.select_custom_or_default_play('mulligan')


        # GAME
        while self.app_status.screen == 'Playing':
            self.game_dict.wait_action()

            # ZONE 27
            if self.game_dict.stack:
                Zone27.solve(self.game_dict.stack)

            # HERO TURN
            if self.game_dict.hero_turn:

                if self.game_dict.phase == 'Phase_Beginning':
                    self.execute.space()

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
                    self.execute.space()

            # TURNO OPONENTE

            elif self.game_dict.phase == 'Phase_Combat' and self.game_dict.step == 'Step_DeclareBlock':
                self.execute.space()

            else:
                self.execute.space()

            if not self.game_dict.active and not self.game_dict.hero_turn:
                self.execute.scan_hand()

        time.sleep(0.7)

        while self.app_status.screen == 'Confused':
            self.execute.concede()
            time.sleep(2)

    # Try to find custom play function otherwise it uses the default one. If none of them exist, it presses space to advance to the next phase.
    def select_custom_or_default_play(self, phase_name):
        # Execute custom/default play_phase_function and then advance to the phase returned by that function
        play_method = getattr(self.mode, phase_name, None) or getattr(self.default_mode, phase_name, None)

        if play_method is None:
            self.execute.space()
            return

        self.advance_to_phase(play_method())

    def advance_to_phase(self, phase):
        if phase not in self.phases:
            return False
        self.game_dict.wait_action()
        if self.game_dict.hero_turn and self.phases.index(phase) > self.phases.index(self.game_dict.phase):
            self.execute.space()
            time.sleep(0.7)


