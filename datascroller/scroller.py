import os
import curses
import pandas as pd
import time

#--------
# poor man's config file
ENTER = 10 
QUIT = 113

SCROLL_LEFT = 104
SCROLL_RIGHT = 108
SCROLL_DOWN = 106
SCROLL_UP = 107

EXPAND_ROW = 120
RETRACT_ROW = 119
EXPAND_COL = 100
RETRACT_COL = 97 

PAGE_DOWN = 6
PAGE_UP = 2

#--------


def get_key_and_print(stdscr, disp_str):
    curses.curs_set(0)
    stdscr.clear()
    stdscr.addstr(5, 5, disp_str)
    stdscr.refresh()
    key = -1
    while key == -1:
        key = stdscr.getch()
    return key

def pdscroller(df, width=5, height=8):
    # Tunable Params
    # Initialization
    last_row = df.shape[0] - 1
    last_col = df.shape[1] - 1

    # Initializing the window
    start_row = 0
    end_row = min(height, last_row)
    start_col = 0
    end_col = min(width, last_col)

    key = -99
    # The scroller loop
    while key not in [ENTER, QUIT]: # Enter or 'q' quits (on my machine at least)
        df_window = df.iloc[start_row:end_row, start_col:end_col]
        key = curses.wrapper(get_key_and_print, df_window.to_string())
        # Movement based on vim keys
        if key in [SCROLL_LEFT, curses.KEY_LEFT] and start_col > 0:
            start_col -= 1
            end_col -= 1
        elif key in [SCROLL_RIGHT, curses.KEY_RIGHT] and start_col + width <= last_col:
            start_col += 1
            end_col += 1
        elif key in [SCROLL_DOWN, curses.KEY_DOWN] and start_row + height <= last_row:
            start_row += 1
            end_row += 1
        elif key in [SCROLL_UP, curses.KEY_UP] and start_row > 0:
            start_row -= 1
            end_row -= 1
        # Window resizing
        elif key == RETRACT_COL and end_col > 0: # Wind window back left - a key
            end_col -= 1
        elif key == EXPAND_COL and end_col <= last_col: # Extend window right - d key
            end_col += 1
        elif key == EXPAND_ROW and end_row <= last_row: # Extend window down - x key
            end_row += 1
        elif key == RETRACT_ROW and end_row > 0: # Wind window back up - w key
            end_row -= 1
        # Moving fast
        elif key == PAGE_DOWN and end_row + height <= last_row: # Ctrl + F
            # TODO: allow for traveling the remainder
            start_row += height
            end_row += height

        elif key == PAGE_UP and start_row - height >= 0: # Ctrl + B
            # TODO: allow for traveling the remainder
            start_row -= height
            end_row -= height

    #return df_window
