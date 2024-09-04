class TurnInfo:

    def __init__(self):
        self.game_state = {}


    @property
    def hero_turn(self):
        return self.hero_seat_id == self.game_state.get('turnInfo', {}).get('activePlayer', False)

    @property
    def active(self):
        return self.hero_seat_id == self.game_state.get('turnInfo', {}).get('decisionPlayer', False)

    @property
    def turn(self):
        return self.game_state.get('turnInfo', {})

    @property
    def phase(self):
        return self.turn.get('phase')

    @property
    def step(self):
        return self.turn.get('step')

    @property
    def next_step(self):
        return self.turn.get('nextStep')

    @property
    def declare_attackers_phase(self):
        # If next step is Declare blocks you've just submitted your attacks and are just before that step,
        # if you are declaring the attackers the next step should be end combat (i think so)
        return True if self.step == 'Step_DeclareAttack' and self.next_step != 'Step_DeclareBlock' else False
