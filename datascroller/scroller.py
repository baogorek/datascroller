import os
import curses
import pandas as pd

def get_key_and_print(stdscr, disp_str):
    curses.curs_set(0)
    stdscr.clear()
    stdscr.addstr(5, 5, disp_str)
    stdscr.refresh()
    while True:
        key = stdscr.getch()
        if key != -1:
            break
    return key

def scroller(df, width=5, height=8): # ignores df for now. Uses iris
    # Tunable Params
    # Initialization
    last_row = df.shape[0] - 1
    last_col = df.shape[1] - 1
    print(last_col)

    # Initializing the window
    start_row = 0
    end_row = min(height, last_row)
    start_col = 0
    end_col = min(width, last_col)

    key = -99
    # The scroller loop
    while key not in [10, 113]: # Enter or 'q' quits (on my machine at least)
        df_window = df.iloc[start_row:end_row, start_col:end_col]
        key = curses.wrapper(get_key_and_print, df_window.to_string())
        # Movement based on vim keys
        if key == 104 and start_col > 0: # h - vim key for left
            start_col -= 1
            end_col -= 1
        elif key == 108 and start_col + width <= last_col: # l - vim key for right #TODO: rewrite condition in terms of end?
            start_col += 1
            end_col += 1
        elif key == 106 and start_row + height <= last_row: # j - vim key for down
            start_row += 1
            end_row += 1
        elif key == 107 and start_row > 0: # k - vim key for up
            start_row -= 1
            end_row -= 1
        # Window resizing
        elif key == 97 and end_col > 0: # Wind window back left - a key
            end_col -= 1
        elif key == 100 and end_col <= last_col: # Extend window right - d key
            end_col += 1
        elif key == 120 and end_row <= last_row: # Extend window down - x key
            end_row += 1
        elif key == 119 and end_row > 0: # Wind window back up - w key
            end_row -= 1
        # Moving fast
        elif key == 6 and end_row + height <= last_row: # Ctrl + F
            # TODO: allow for traveling the remainder
            start_row += height
            end_row += height

        elif key == 2 and start_row - height >= 0: # Ctrl + B
            # TODO: allow for traveling the remainder
            start_row -= height
            end_row -= height

    return df_window
