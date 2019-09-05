import os
import curses
import pandas as pd
import time


# poor man's config file ------------------------------------------------------
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
#------------------------------------------------------------------------------


def get_key_and_print(stdscr, disp_str):
    curses.curs_set(0)
    stdscr.clear()
    stdscr.addstr(5, 5, disp_str)
    stdscr.refresh()
    key = -1
    while key == -1:
        key = stdscr.getch()
    return key


def key_press_and_print_df(stdscr, df):
    curses.curs_set(0)
    max_yx = stdscr.getmaxyx() # NOTE: This does not change in real time
    last_row = df.shape[0] - 1
    last_col = df.shape[1] - 1

    # Initializing the window
    start_row = 0
    end_row = min(5, last_row,  max_yx[0] - 1) # TODO (ben): make configurable
    start_col = 0
    end_col = min(10, last_col)

    # Turn dataframe window into pritable string
    df_window = df.iloc[start_row:end_row, start_col:end_col]
    disp_str = df_window.to_string()
    row_chars = len(disp_str.split('\n')[0])
    while row_chars > max_yx[1] - 1:
        end_col -= 1
        df_window = df.iloc[start_row:end_row, start_col:end_col]
        disp_str = df_window.to_string()
        row_chars = len(disp_str.split('\n')[0])

    stdscr.clear()
    stdscr.addstr(0, 0, disp_str)
    stdscr.refresh()

    key = -1
    # The scroller loop
    while key not in [ENTER, QUIT]:

        key = stdscr.getch()

        # Movement based on vim keys
        if key in [SCROLL_LEFT, curses.KEY_LEFT] and start_col > 0:
            start_col -= 1
            end_col -= 1
        elif key in [SCROLL_RIGHT, curses.KEY_RIGHT] and start_col < last_col:
            start_col += 1
            end_col += 1
        elif key in [SCROLL_DOWN, curses.KEY_DOWN] and start_row < last_row:
            start_row += 1
            end_row += 1
        elif key in [SCROLL_UP, curses.KEY_UP] and start_row > 0:
            start_row -= 1
            end_row -= 1
        # Window resizing
        elif key == RETRACT_COL and end_col > 0:
            end_col -= 1
        elif key == EXPAND_COL and end_col < last_col:
            end_col += 1
        elif key == EXPAND_ROW and end_row < last_row:
            end_row += 1
        elif key == RETRACT_ROW and end_row > 0:
            end_row -= 1
        # Moving fast
        elif key == PAGE_DOWN and end_row < last_row:
            height = end_row - start_row
            start_row += height
            end_row += height 

        elif key == PAGE_UP and end_row - (end_row - start_row) >= 0:
            height = end_row - start_row
            start_row -= height 
            end_row -= height 
        # After all the if & elif statements, reprint and display
        disp_str = df.iloc[start_row:end_row, start_col:end_col].to_string()
        stdscr.clear()
        stdscr.addstr(0, 0, disp_str)
        stdscr.addstr(0, 0, 'R' + str(start_row))
        stdscr.refresh()


def scroll(scrollable):
    if isinstance(scrollable, pd.core.frame.DataFrame):
        curses.wrapper( key_press_and_print_df, scrollable)
    else:
        print('type ' + str(type(scrollable)) + ' not yet scrollable!')


def main():
    # This is how you run scroller2
    #load_ext autoreload
    #autoreload 2
    #import pandas as pd
    #from datascroller import scroll
    train = pd.read_csv('resources/train.csv')
    scroll(train)

if __name__ == '__main__':
    main()
