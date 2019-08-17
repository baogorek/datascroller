import time
import curses

def main(stdscr):
    curses.curs_set(0)
    stdscr.addstr(5, 50, 'Hello')
    stdscr.refresh()
    time.sleep(3)

curses.wrapper(main)

def main(stdscr):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_YELLOW) # Initializing a id / foregroud / background color pair
    stdscr.attron(curses.color_pair(1)) # Screen "Attribute On" for the color pair

    h, w = stdscr.getmaxyx()
    text = "Hello, World!"

    x = w // 2 - len(text) // 2
    y = h // 2

    stdscr.addstr(y, x, text)
    stdscr.attroff(curses.color_pair(1)) # Screen "Attribute Off" for the color pair
    stdscr.refresh()
    time.sleep(3)

curses.wrapper(main)

import curses
import time

def main(stdscr):
    curses.curs_set(0)
    while True:
        key = stdscr.getch()

        stdscr.clear()
        if key == curses.KEY_UP:
            stdscr.addstr(0, 0, "You pressed up key!")
        elif key == curses.KEY_DOWN:
            stdscr.addstr(0, 0, "You pressed down key!")
        elif key == curses.KEY_ENTER or key in [10, 13]:
            stdscr.addstr(0, 0, "You pressed Enter!")
        stdscr.addstr(10, 0, "Integer value of key is : " + str(key)) 
        stdscr.refresh()
    return key

curses.wrapper(main)

stdscr = curses.initscr() # initialize a terminal screen and return a window object
#
#curses.noecho()  # Don't print the character that you type like usual terminals
curses.cbreak()  # As soon as the user presses a key, the value is returned to the program 
#stdscr.keypad(True) # Treats special keys as special values
#
#stdscr.addstr(5, 50, 'Hello')
#stdscr.refresh()
#time.sleep(3)
#
# curses.curs_set(1) # makes cursor blink, 0 would be no blinking
curses.echo()
#curses.nocbreak()
#stdscr.keypad(False)
#
curses.endwin() # closes window
