import curses
import time
import argparse

from datascroller import scroll, scroll_csv, demo


def getkey(stdscr):
    curses.curs_set(0)
    # curses.halfdelay(1) # Half-delay mode => getch blocks for x tenths of sec
    stdscr.nodelay(1)  # NoDelay mode on => getch is non-blocking
    stdscr.addstr(0, 0, 'Press a key, any key!')
    stdscr.refresh()
    while True:
        key1 = stdscr.getch()
        key2 = stdscr.getch()
        if key1 != -1:
            break
        time.sleep(.3)
    return key1, key2


def run_getkey():
    key1, key2 = curses.wrapper(getkey)
    print('The curses keycode is ' + str(key1) + ' and ', str(key2))


def run_demo():
    df = demo.read_titanic()
    scroll(df)


def run_scroll():
    parser = argparse.ArgumentParser(
        description="""Scroll a CSV from the command line with datascroller

            The following keys are currently supported:
            # Movement
              - h: move to the left
              - j: move down
              - k: move up
              - l: move left
            # Quick Movement
              - Ctrl + F: Page down
              - Ctrl + B: Page up (not working as well for some reason)
            # Exiting
              - q
        """, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('csv_filepath',
                        help='a csv filepath, relative or absolute')
    parser.add_argument("-s", "--sep", choices=[',', '|', ';', ':', ' ', '\t'], default=',""',
                        help="csv separator, choose between ',', '|', ';', ':', ' ', '\\t'")
    parser.add_argument("-e", "--enc", choices=['utf_8', 'utf_7', 'utf_16', 'utf_32'], default='utf_8',
                        help="csv separator, choose between 'utf_8', 'utf_7', 'utf_16', 'utf_32'")
    args = parser.parse_args()
    scroll_csv(args.csv_filepath, args.sep, args.enc)
