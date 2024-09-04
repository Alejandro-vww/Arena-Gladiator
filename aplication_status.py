import time
from game_dict import GameDict

max_playing_time = 30 * 60
max_active_time = 30
max_screen_time = 5 * 60


class AplicationStatus:
    _instance = None
    _screen = None    #Home..., Playing, GameEnded, (Bugged)
    _win = None
    mulligan = False

    last_actualization = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.game_dict = GameDict()
        self.last_active_game_state = {'id': 0, 'time': time.time()}

    @property
    def win(self):
        if self._win:
            self._win = None
            return True
        elif self._win == False:
            self._win = None
            return False
        else:
            return None

    @win.setter
    def win(self, value):
        self._win = value

    @property
    def screen(self):
        #Too much time in the same screen
        if self.last_actualization:     #actualized with screen setter
            waited = time.time() - self.last_actualization
            max_waiting = max_playing_time if self._screen == 'Playing' else max_screen_time
            if waited > max_waiting:
                # self.last_actualization = None  # Asegura solo devolver una vez el atascado, no vuelve a contabilizar el tiempo hasta recibir nueva actualización del log
                return 'Bugged'

        #Too much time in your turn
        if self.game_dict.active:
            if self.last_active_game_state['id'] == self.game_dict.game_state_id:
                if time.time() - self.last_active_game_state['time'] > max_active_time:
                    return 'Confused'
            else:
                self.last_active_game_state = {'id': self.game_dict.game_state_id, 'time': time.time()}

        return self._screen

    @screen.setter
    def screen(self, value):
        self._screen = value
        self.last_actualization = time.time()

