import time

from log_reader import LogReader
from user_interface import Application


def main():
    app = Application()
    app.mainloop()


if __name__ == "__main__":
    LogReader.start_read()
    #main()





