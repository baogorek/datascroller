import sys
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

class DFWindow:
    """The data frame window"""
    def __init__(self, pandas_df, viewing_area):
        self.full_df = pandas_df
        self.viewing_area = viewing_area

        self.left = viewing_area.pad_x 
        self.right = self.full_df.shape[1]
        self.top = viewing_area.pad_y 
        self.bottom = self.full_df.shape[0]
        self.data = self.full_df

    def build_position_list(self):
        """list of character positions for each variable (x dimension)"""
        positions = []
        for j in range(self.full_df.shape[1]):
           row_str = self.full_df.iloc[1, 0:j].to_string().split('\n')[1]
           positions.append(len(row_str))

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
    def __init__(self, total_chars_y, total_chars_x, pad_y, pad_x):
        """Initialize the real estate of the padded viewing area"""
        self.max_char_y_coord = total_chars_y - 1
        self.max_char_x_coord = total_chars_x - 1

        self.total_chars_y = total_chars_y
        self.total_chars_x = total_chars_x

        self.pad_char_y = pad_y
        self.pad_char_x = pad_x

        self.leftmost_char = pad_x
        self.rightmost_char = self.total_chars_x - pad_x
        self.topmost_char = pad_y
        self.bottommost_char = self.total_chars_y - pad_y

    def _create_list_of_rowstrings(self):
        """prints a representation of the viewing area to aid understanding"""
        row_list = []
        for k in range(self.pad_char_y):
            row_list.append('P' * self.total_chars_x)
        for i in range(self.total_chars_y - 2 * self.pad_char_y):
            row_list.append('P' * self.pad_char_x
                           + 'X' * (self.total_chars_x - 2 * self.pad_char_x)
                           + 'P' * self.pad_char_x)
        for k in range(self.pad_char_y):
            row_list.append('P' * self.total_chars_x)
        return row_list

    def print_representation(self):
        rowlist = self._create_list_of_rowstrings()
        for j in range(self.total_chars_y):
            print(rowlist[j], end='')
            sys.stdout.flush()
        time.sleep(3)

    def _display_string_rep_using_curses(self, screen):
        curses.curs_set(0)
        rowlist = self._create_list_of_rowstrings()
        for j in range(self.total_chars_y):
            screen.addstr(0, j, rowlist[j])
        time.sleep(3)

    def show_curses_representation(self):
        curses.wrapper(self._display_string_rep_using_curses)


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
