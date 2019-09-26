import sys
import os
import shutil
import curses
import pandas as pd
import time

# dev script
#import pandas as pd
#train_df = pd.read_csv('resources/train.csv')
#load_ext autoreload
#autoreload 2
#from datascroller.scroller import *


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


class DFWindow:
    """The data frame window"""
    def __init__(self, pandas_df, viewing_area):
        self.full_df = pandas_df
        self.viewing_area = viewing_area
        self.positions = self.build_position_list()

        # df[r_1:r_2, c_1:c_2]
        self.r_1 = 0
        self.r_2 = viewing_area.max_char_y_coord
        self.c_1 = 0
        self.c_2 = 3 #TODO

        self.df_window = self.full_df.iloc[self.r_1:self.r_2,
                                           self.c_1:self.c_2]

    def get_window_string(self):
        """get a string representation of the window that respects padding

        Another way to handle this would be to print line by line with curses.
        That might be slower. The downside of this approach is that spaces
        will erase any text to the left of the printed window.
        """
        window_string = self.df_window.to_string()
        row_padding = '\n' + ' ' * self.viewing_area.pad_chars_x
        padded_string = window_string.replace('\n', row_padding)
        return padded_string

    def show_data_window_in_viewing_area(self):
        self.viewing_area.show_curses_representation(
                self.get_window_string())

    def build_position_list(self):
        """list of character positions for each variable (x dimension)"""
        positions = []
        for j in range(1, self.full_df.shape[1] + 1):
           row_str = self.full_df.iloc[0:2, 0:j].to_string().split('\n')[-1]
           positions.append(len(row_str))
        return positions

    def update(self):
        self.data = self.full_df[self.top:self.bottom, self.left:self.right]

    def get_horizontal_strlen(self):
        return len(self.print().split('\n')[0])
    
    def get_vertical_strlen(self):
        return self.bottom - self.top
    
    def old_code_probably_delete(self):
        # Turn dataframe window into pritable string
        df_window = df.iloc[start_row:end_row, start_col:end_col]
        disp_str = df_window.to_string()
        row_chars = len(disp_str.split('\n')[0])
        while row_chars > max_yx[1] - 1:
            end_col -= 1
            df_window = df.iloc[start_row:end_row, start_col:end_col]
            disp_str = df_window.to_string()
            row_chars = len(disp_str.split('\n')[0])


    def print(self):
        return self.data.to_string()

    def move_right(self):
        pass

    def move_left(self):
        pass

    def move_down(self):
        pass

    def move_up(self):
        pass
    
    def fit_within_char_dimensions(self, str_y, str_x):
        pass


class ViewingArea:
    """ Class representing the viewing area where dataframes are printed

        This class is specifically designed to minimize confusion. It takes 
        as input pane dimensions but calculates seemingly trivial quantities
        like the maximum coordinates (1 less). The show and print methods
        provide a sanity check to the developer in later stages.

        Attributes
        ----------
        max_char_x_coord : int
            The maximum curses coordinate for the col dimension, padded area
        max_char_y_coord : int
            The maximum curses coordinate for the row dimension, padded area
        total_chars_x: int
            The vertical pane dimension
        total_chars_y: int
            The horizonal pane dimension
        pad_chars_x: int
            The amount of black spaces at the top and bottom
        pad_chars_y: int
            The amount of blank spaces to the left and right
        leftmost_char: int
            The leftmost x coordinate value where there can be output
        rightmost_char: int
            The rightmost x coordinate value where there can be output
        topmost_char: int
            The topmost y coordinate value where there can be output
        bottommost_char: int
            The bottommost y coordinate value where there can be output

        Methods
        -------
        print_representation()
            prints a representation of the viewing area without curses
        show_curses_representation()
            displays a representation of the viewing area using curses,
            and also displays the corners of the content bounding box.
        """
    def __init__(self, pad_x, pad_y):
        """Initialize the real estate of the padded viewing area
    
        Parameters
        ----------
        pad_chars_x: int
            The amount of black spaces at the top and bottom
        pad_chars_y: int
            The amount of blank spaces to the left and right
        """
        self.pad_chars_x = pad_x
        self.pad_chars_y = pad_y

        term_size = shutil.get_terminal_size()
        self.total_chars_x = term_size.columns
        self.total_chars_y = term_size.lines

        self.max_char_x_coord = self.total_chars_x - 2 * self.pad_chars_x - 1
        self.max_char_y_coord = self.total_chars_y - 2 * self.pad_chars_y - 1

        self.leftmost_char = pad_x
        self.rightmost_char = self.total_chars_x - pad_x - 1
        self.topmost_char = pad_y
        self.bottommost_char = self.total_chars_y - pad_y - 1

    def _create_list_of_rowstrings(self):
        """prints a representation of the viewing area to aid understanding"""
        row_list = []
        for k in range(self.pad_chars_y):
            row_list.append('P' * self.total_chars_x)
        for i in range(self.total_chars_y - 2 * self.pad_chars_y):
            row_list.append('P' * self.pad_chars_x
                           + 'X' * (self.total_chars_x - 2 * self.pad_chars_x)
                           + 'P' * self.pad_chars_x)
        for k in range(self.pad_chars_y):
            row_list.append('P' * self.total_chars_x)
        return row_list

    def print_representation(self):
        rowlist = self._create_list_of_rowstrings()
        for j in range(self.total_chars_y - 1):
            print(rowlist[j])
        print(rowlist[self.total_chars_y - 1], end='')
        sys.stdout.flush()
        time.sleep(3)

    def _display_string_rep_using_curses(self, screen, otherstring=None):
        curses.curs_set(0)
        rowlist = self._create_list_of_rowstrings()
        screen.clear()
        screen.refresh()
        for j in range(self.total_chars_y):
            try:
                screen.addstr(j, 0, rowlist[j])
            except curses.error:
                # Last x-char: still prints character even with error
                pass
        screen.refresh()
        time.sleep(1)
        curses.curs_set(1)

        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_YELLOW) # id 1
        screen.attron(curses.color_pair(1))

        screen.addstr(self.topmost_char, self.leftmost_char, 'A')
        screen.refresh()
        time.sleep(1)

        screen.addstr(self.topmost_char, self.rightmost_char, 'B')
        screen.refresh()
        time.sleep(1)

        screen.addstr(self.bottommost_char, self.leftmost_char, 'C')
        screen.refresh()
        time.sleep(1)

        screen.addstr(self.bottommost_char, self.rightmost_char, 'D')
        screen.refresh()
        time.sleep(3)

        if otherstring:
            screen.addstr(self.topmost_char, self.leftmost_char,
                          otherstring)
            screen.refresh()
            time.sleep(3)

        screen.attroff(curses.color_pair(1))
        curses.endwin() # NOTE: Still not sure about the persistance of screen

    def show_curses_representation(self, otherstring=None):
        curses.wrapper(self._display_string_rep_using_curses, otherstring)


def key_press_and_print_df(stdscr, df):
    curses.curs_set(0)

    viewing_area = ViewingArea(stdscr, 2, 4) 
    df_window = DFWindow(df)

    stdscr.clear()
    stdscr.addstr(pad_y, pad_x, disp_str)
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
        elif key == curses.KEY_RESIZE:
            print("Terminal resized. Please restart scroller")
            break
        # After all the if & elif statements, reprint and display
        disp_str = df.iloc[start_row:end_row, start_col:end_col].to_string()

        # TODO(baogore): Violating DRY principle - encapsulate
        row_chars = len(disp_str.split('\n')[0])
        while row_chars > max_yx[1] - 1:
            end_col -= 1
            df_window = df.iloc[start_row:end_row, start_col:end_col]
            disp_str = df_window.to_string()
            row_chars = len(disp_str.split('\n')[0])

        stdscr.clear()
        stdscr.addstr(0, 0, disp_str)
        stdscr.addstr(0, 0, 'R' + str(start_row))
        stdscr.refresh()


def scroll(scrollable):
    if isinstance(scrollable, pd.core.frame.DataFrame):
        curses.wrapper(key_press_and_print_df, scrollable)
    else:
        print('type ' + str(type(scrollable)) + ' not yet scrollable!')

def scroll_csv(csv_path):
    pandas_df = pd.read_csv(csv_path)
    scroll(pandas_df)

def main():
    scroll_csv(sys.argv[1])

if __name__ == '__main__':
    main()
