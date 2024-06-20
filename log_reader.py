import time
import tkinter as tk
from tkinter import filedialog
import logging, logging.config
from json_to_dict import JsonToDict
from game_dict import GameDict

class LogReader:

    def __init__(self):
        self.game_dict = GameDict()
        self._start_reading()

    def _start_reading(self):
        player_log = self._open_log()
        player_log.seek(0)

        while True:
            line = None
            try:
                line = player_log.readline()
            except Exception as e:
                log_exception.error()

            if not line:
                time.sleep(0.5)
                continue

            transaction = JsonToDict.get_dict(line)

            self.game_dict.update(transaction) if transaction else None

    def _open_log(self):
        """
        Returns:
            _io.TextIOWrapper: 'Player.log'.

        Raises:
            FileNotFoundError: If 'Player.log' is not found.
        """

        try: #Open 'Player.log' saved path
            return open('C:\\Users\\TONTO\\AppData\\LocalLow\\Wizards Of The Coast\\MTGA\\Player.log', 'r', errors='ignore')

        except FileNotFoundError:
            # Open file dialog to select Player.log file
            root = tk.Tk()
            root.withdraw()  # Create an hidden window
            file_path = filedialog.askopenfilename(title="'Player.log' no encontrado")
            if file_path:
                return open(file_path, 'r', errors='ignore')
            else:
                raise FileNotFoundError("'Player.log' no encontrado")




logging.config.fileConfig('config\logging.conf')
log_exception = logging.getLogger('Exceptions')


if __name__ == '__main__':
    log_reader = LogReader()
    log_reader._open_log()
