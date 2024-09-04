import win32gui, win32api, win32con
import os
import tkinter as tk
from tkinter import filedialog
import time
from aplication_status import AplicationStatus



# from win32api import GetSystemMetrics GetSystemMetrics(0) = width // GetSystemMetrics(1) = height


#Necesita el nombre aproximado para sacar dimensiones de la ventana

class Window:

    #Hay 8 píxeles de borde (-8 al +8)
    _top = None
    _bot = None
    _right = None
    _left = None
    _width = None
    _height = None

    screen_width = win32api.GetSystemMetrics(0)
    screen_height = win32api.GetSystemMetrics(1)

    status = AplicationStatus()

    def __init__(self):
        if not self.hwnd:
            self.open()
        from game_window.executor import Executor
        self.execute = Executor()

    @property
    def hwnd(self):
        window_name = 'MTGA'
        hwnd = win32gui.FindWindow(None, window_name)
        if hwnd:
            return hwnd
        else:
            return False

    def open(self):
        file_path = "C:\Program Files\Wizards of the Coast\MTGA\MTGALauncher\MTGALauncher.exe"

        if os.path.isfile(file_path):
            os.startfile(file_path)
        else:
            root = tk.Tk()
            root.withdraw()  # Create an hidden window
            file_path = filedialog.askopenfilename(title="'MTGALaunchrer.exe' no encontrado")
            if os.path.isfile(file_path):
                os.startfile(file_path)
            else:
                raise FileNotFoundError("'MTGALaunchrer.exe' no encontrado")

    def close(self):
        if self.hwnd:
            win32gui.PostMessage(self.hwnd, win32con.WM_CLOSE, 0, 0)

    def restart(self):
        self.close()
        time.sleep(3)
        self.open()
        time.sleep(30)

    def check_status(self):
        if not self.hwnd:
            self.open()
            time.sleep(30)
        
        if self.status.screen == 'Confused':
            self.execute.concede()
            
        elif self.status.screen == 'Bugged':
            self.restart()
            for _ in range(180):
                if self.status.screen != 'Bugged':
                    break
                time.sleep(1)

    @property
    def top(self):
        self.check_status()
        self._left, self._top, self._right, self._bot = win32gui.GetWindowRect(self.hwnd)
        return self._top + 30

    @property
    def bot(self):
        self.check_status()
        self._left, self._top, self._right, self._bot = win32gui.GetWindowRect(self.hwnd)
        return self._bot - 8

    @property
    def right(self):
        self.check_status()
        self._left, self._top, self._right, self._bot = win32gui.GetWindowRect(self.hwnd)
        return self._right - 8

    @property
    def left(self):
        self.check_status()
        self._left, self._top, self._right, self._bot = win32gui.GetWindowRect(self.hwnd)
        return self._left + 8

    @property
    def width(self):
        self.check_status()
        self._left, self._top, self._right, self._bot = win32gui.GetWindowRect(self.hwnd)
        return self._right - self._left - 16

    @property
    def height(self):
        self.check_status()
        self._left, self._top, self._right, self._bot = win32gui.GetWindowRect(self.hwnd)
        return self._bot - self._top - 38



    @property
    def unchecked_top(self):
        self._left, self._top, self._right, self._bot = win32gui.GetWindowRect(self.hwnd)
        return self._top + 30

    @property
    def unchecked_bot(self):
        self._left, self._top, self._right, self._bot = win32gui.GetWindowRect(self.hwnd)
        return self._bot - 8

    @property
    def unchecked_right(self):
        self._left, self._top, self._right, self._bot = win32gui.GetWindowRect(self.hwnd)
        return self._right - 8

    @property
    def unchecked_left(self):
        self._left, self._top, self._right, self._bot = win32gui.GetWindowRect(self.hwnd)
        return self._left + 8

    @property
    def unchecked_width(self):
        self._left, self._top, self._right, self._bot = win32gui.GetWindowRect(self.hwnd)
        return self._right - self._left - 16

    @property
    def unchecked_height(self):
        self._left, self._top, self._right, self._bot = win32gui.GetWindowRect(self.hwnd)
        return self._bot - self._top - 38



if __name__ == '__main__':
    captura = Window()
    captura.restart()