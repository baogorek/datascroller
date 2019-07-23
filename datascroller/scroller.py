import os
import curses

import statsmodels as sm
import statsmodels.api as smapi

# Alternate names:
# scrolldf
# pdscroller

iris = smapi.datasets.get_rdataset('iris').data

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

def scroller(df): # ignores df for now. Uses iris
    # Tunable Params
    # ?
    # Initialization
    start_row = 0
    end_row = min(5, df.shape[0])
    start_col = 0
    end_col = min(3, df.shape[1])
    key = -99
    # The scroller loop
    while key not in [10, 113]: # Enter or 'q' quits (on my machine at least)
        df_window = df.iloc[start_row:end_row, start_col:end_col]
        key = curses.wrapper(get_key_and_print, df_window.to_string())
        if key == 104:
            start_col -= 1
            end_col -= 1
        elif key == 106:
            start_col += 1
            end_col += 1
    return df_window

scroller(iris) # Start by pressing the "j" key a couple of times, then press "h"

if __name__ == "__main__":
    print("Run scroller(df) in ipython")
    print("h and j keys to move")
