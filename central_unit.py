from multiprocessing import Process
import time

from arena_gladiator import ArenaGladiator
from game_window.executor import Executor


execute = Executor()
arena_gladiator = ArenaGladiator()

start_game = Process(target=execute.start_game)
play_game = Process(target=arena_gladiator.play)

total_wins = 1

if __name__ == '__main__':
    wins = 0
    time.sleep(20)
    if exe.window.status.win:
        pass
    while total_wins > wins:
        time.sleep(0.2)
        if exe.window.status.screen != 'Playing':
            exe.start_game()
        else:
            arena.play()
            time.sleep(0.6)
        if exe.window.status.win:
            wins += 1
    print('victorias completadas')
