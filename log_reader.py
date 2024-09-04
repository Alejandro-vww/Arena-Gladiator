import time
import tkinter as tk
from tkinter import filedialog
from json_to_dict import JsonToDict
from message_processor import MessageProcessor
import threading
import os
from user_config import log_path


class LogReader:

    msg_processor = MessageProcessor()

    @staticmethod
    def start_read():
        thread = threading.Thread(target=LogReader._reader)
        thread.start()

    @staticmethod
    def _reader():
        player_log, file_path_used = LogReader._open_log()
        while True:
            current_inode = os.stat(file_path_used).st_ino
            last_size = os.path.getsize(file_path_used)
            player_log.seek(0)
            while current_inode == os.stat(file_path_used).st_ino:
                if last_size > os.path.getsize(file_path_used):
                    player_log.seek(0)
                last_size = os.path.getsize(file_path_used)

                line = None
                try:
                    line = player_log.readline()
                except Exception as e:
                    print("Can't read line")
                if not line:
                    time.sleep(0.5)
                    continue

                if __name__ == '__main__':
                    print(line)

                transaction = JsonToDict.get_dict(line)
                LogReader.msg_processor.update(transaction) if transaction else None

            player_log, file_path_used = LogReader._open_log(file_path=file_path_used)

    @staticmethod
    def _open_log(file_path=log_path):
        try: #Open 'Player.log' saved path
            return open(file_path, 'r', errors='ignore'), file_path

        except FileNotFoundError:
            # Open file dialog to select Player.log file
            root = tk.Tk()
            root.withdraw()  # Create an hidden window
            file_path = filedialog.askopenfilename(title="'Player.log' no encontrado")
            if file_path:
                return open(file_path, 'r', errors='ignore'), file_path
            else:
                raise FileNotFoundError("'Player.log' no encontrado")


if __name__ == '__main__':
    LogReader.start_read()
    while True:
        time.sleep(1)




