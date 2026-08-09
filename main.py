import time

from arena_gladiator import ArenaGladiator
from game.controller.executor import Executor
from game.mtga_log_reader.log_reader import LogReader
from minion_of_the_mighty import MinionOfTheMighty
from user_interface import Application


def main():
    app = Application()
    app.mainloop()


if __name__ == "__main__":
    LogReader.start_read()
    # arena_gladiator = ArenaGladiator(custom_mode=MinionOfTheMighty)
    arena_gladiator = ArenaGladiator()
    execute = Executor()
    time.sleep(10)

    games_won = 0

    while True:
        if execute.window.status.screen != 'Playing':
            execute.start_game()
        if execute.window.status.screen == 'Playing':
            arena_gladiator.play()
            time.sleep(1)
        if execute.window.status.win:
            games_won += 1
            print(f'Games won: {games_won}')





