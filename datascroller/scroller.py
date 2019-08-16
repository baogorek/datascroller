import os
import curses
import pandas as pd

# Alternate names:
# scrolldf
# pdscroller

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
    # ?
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
        if key == 104 and start_col > 0: # h - vim key for left
            start_col -= 1
            end_col -= 1
        elif key == 108 and start_col + width <= last_col: # l - vim key for right
            start_col += 1
            end_col += 1
        elif key == 106 and start_row + height <= last_row: # j - vim key for down
            start_row += 1
            end_row += 1
        elif key == 107 and start_row > 0: # k - vim key for up
            start_row -= 1
            end_row -= 1
       # j is down: 106, k is up, 107, h is left, 104, l is right - 108
    return df_window

train = pd.read_csv('train.csv')

scroller(train.tail(50)) # Start by pressing the "j" key a couple of times, then press "h"

if __name__ == "__main__":
    print("Run scroller(df) in ipython")
    print("h and j keys to move")
