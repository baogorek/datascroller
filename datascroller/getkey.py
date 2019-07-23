import curses

def getkey(stdscr):
    curses.curs_set(0)
    while True:
        key = stdscr.getch()
        if key != -1:
            break
    return key

if __name__ == "__main__":
 print(curses.wrapper(getkey))
