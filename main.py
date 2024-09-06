import time

from arena_gladiator import ArenaGladiator
from game_dict import GameDict
from game_window.executor import Executor
from log_reader import LogReader

arena_gladiator = ArenaGladiator()
execute = Executor()

if __name__ == '__main__':
    LogReader.start_read()
    while True:
        execute.start_game()
        arena_gladiator.play()
        time.sleep(1)
        if execute.window.status.win:
            print('win')







