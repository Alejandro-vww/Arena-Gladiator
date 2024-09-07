import os
import time
from pynput import keyboard


# Playing function
def playing_function(total_victories, power_off):
    from arena_gladiator import ArenaGladiator
    from game_window.executor import Executor
    from log_reader import LogReader

    LogReader.start_read()
    arena_gladiator = ArenaGladiator()
    execute = Executor()
    time.sleep(20)

    games_won = 0

    while total_victories > games_won:
        if execute.window.status.screen != 'Playing':
            execute.start_game()
        if execute.window.status.screen == 'Playing':
            arena_gladiator.play()
            time.sleep(1)
        if execute.window.status.win:
            games_won += 1
            print(f'Games won: {games_won}')

    if power_off:
        os.system("shutdown /s /t 0")


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

