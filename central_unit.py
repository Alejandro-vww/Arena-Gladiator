import time
from pynput import mouse, keyboard
from user_config import min_afk_time
from exceptions import EscPressedError



# Playing function
total_wins = 1
games_won = 0
first_execution = True


def set_total_wins(wins):
    global total_wins
    total_wins = wins


def victories_fulfilled():
    return True if games_won >= total_wins else False


# Exit when 'esc' is pressed listener
stop = False


def on_press(key):
    global stop
    if key == keyboard.Key.esc:
        stop = True


keyboard_listener = keyboard.Listener(on_press=on_press)


def start_listeners():
    keyboard_listener.start()


def stop_listeners():
    keyboard_listener.stop()

