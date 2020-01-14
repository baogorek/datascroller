import sys
import shutil
import curses
import pandas as pd
import time


# hard-coded config TODO(baogorek): allow config file -------------------------
ENTER = 10
QUIT = 113

SCROLL_LEFT = 104
SCROLL_RIGHT = 108
SCROLL_DOWN = 106
SCROLL_UP = 107

PAGE_DOWN = 6
PAGE_UP = 2
# ------------------------------------------------------------------------------


class DFWindow:
    """The data frame window"""

    def __init__(self, pandas_df, viewing_area):
        self.full_df = pandas_df
        (self.total_rows, self.total_cols) = pandas_df.shape

        self.viewing_area = viewing_area
        self.positions = self.build_position_list()
        self.rows_to_print = (self.viewing_area.bottommost_char -
                              self.viewing_area.topmost_char + 1)

        self.update_dataframe_coords()

    def get_dataframe_window(self):
        """DataFrame window of form self.df[r_1:r_2, c_1:c_2]"""
        return self.full_df.iloc[self.r_1:self.r_2, self.c_1:self.c_2]

    def get_window_string(self):
        """get a string representation of the window that respects padding

        Another way to handle this would be to print line by line with curses.
        That might be slower. The downside of this approach is that spaces
        will erase any text to the left of the printed window.
        """
        self.df_window = self.get_dataframe_window()
        window_string = self.df_window.to_string()
        row_padding = '\n' + ' ' * self.viewing_area.pad_chars_x
        padded_string = window_string.replace('\n', row_padding)
        return padded_string

    def get_location_string(self):
        """Creates a header showing where the top left df corner is"""
        # TODO (baogorek): Handle thousands and millions
        location_string = ('Rows ' +
                           str(self.r_1) +
                           '-' +
                           str(self.r_2) +
                           ' of ' +
                           str(self.total_rows) +
                           '\nCols ' +
                           str(self.c_1) +
                           '-' +
                           str(self.c_2) +
                           ' of ' +
                           str(self.total_cols))

        return location_string

    def update_dataframe_coords(self, start_row=0, start_col=0):
        self.r_1 = start_row
        self.c_1 = start_col
        self.r_2 = self.r_1 + self.rows_to_print
        self.c_2 = self.find_last_fitting_column()

    def show_data_window_in_viewing_area(self):  # start_row=0, start_col=0):
        self.viewing_area.show_curses_representation(
            self.get_window_string())

    def show_data_on_screen(self, screen):
        self.viewing_area.show_on_screen(screen, self.get_window_string())

    def add_data_to_screen(self, screen):
        self.viewing_area.add_to_screen(screen, self.get_window_string())

    def find_last_fitting_column(self):
        """Finds the largest self.c_1 value s.t. window fits in pane

        It is important to test the positions with the actual rows, since
        certain values that may or may not appear will change the size of
        the printing window.
        """
        k = self.c_1
        row_len = 0
        while ((k <= self.full_df.shape[1]) and
                (row_len + self.viewing_area.pad_chars_x
                    <= self.viewing_area.rightmost_char)):
            k = k + 1
            row_len = len(self.full_df
                              .iloc[self.r_1:self.r_2, self.c_1:k]
                              .to_string().split('\n')[-1])
        return k - 1

    def build_position_list(self):
        """list of cumulative character for each variable (x dimension)

        Most useful to printing are positions of where the columns end,
        not where the columns start.

        For instance, `df2 = pd.DataFrame([['red', 'blue']])` would lead
        to a position list of 6 and 12, given the 4 characters for the
        index, and also the whitespace characters for spacing.

        NOTE: This method is no longer used since find_last_fitting_column
        was changed. Deprecated.
        """
        positions = []
        for j in range(1, self.full_df.shape[1] + 1):
            row_str = self.full_df.iloc[0:2, 0:j].to_string().split('\n')[-1]
            positions.append(len(row_str))
        return positions

    def move_right(self):
        if self.c_2 < self.full_df.shape[1]:
            self.update_dataframe_coords(start_row=self.r_1,
                                         start_col=self.c_1 + 1)

    def move_left(self):
        if self.c_1 > 0:
            self.update_dataframe_coords(start_row=self.r_1,
                                         start_col=self.c_1 - 1)

    def move_down(self):
        if self.r_2 < self.full_df.shape[0]:
            self.update_dataframe_coords(start_row=self.r_1 + 1,
                                         start_col=self.c_1)

    def move_up(self):
        if self.r_1 > 0:
            self.update_dataframe_coords(start_row=self.r_1 - 1,
                                         start_col=self.c_1)

    def page_down(self):
        if self.r_2 < self.full_df.shape[0] - 1:
            page_size = self.rows_to_print
            if self.r_1 + page_size > self.full_df.shape[0] - 1:
                page_size = self.full_df.shape[0] - self.r_1 + 1
            self.update_dataframe_coords(start_row=self.r_1 + page_size,
                                         start_col=self.c_1)

    def page_up(self):
        page_size = self.r_2 - self.r_1
        if self.r_1 - page_size < 0:
            page_size = self.r_1
        self.update_dataframe_coords(start_row=self.r_1 - page_size,
                                     start_col=self.c_1)


class ViewingArea:
    """ Class representing the viewing area where dataframes are printed

        This class is specifically designed to minimize confusion. It takes
        as input pane dimensions but calculates seemingly trivial quantities
        like the maximum coordinates (1 less). The show and print methods
        provide a sanity check to the developer in later stages.

        Attributes
        ----------
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

    def _display_string_using_curses(self, screen, otherstring):
        """Prints strings for use with the scroller"""
        try:
            screen.addstr(self.topmost_char, self.leftmost_char,
                          otherstring)
            screen.refresh()
        except curses.error:
            pass

    # TODO(baogorek): figure out what to do with function above
    def _add_string_using_curses(self, screen, otherstring):
        """Prints strings for use with the scroller"""

        # The init_pair(n, f, b) function changes the definition of
        # color pair n, to foreground color f and background color b
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
        # NOTE: see http://tldp.org/HOWTO/NCURSES-Programming-HOWTO/attrib.html
        try:
            screen.addstr(self.topmost_char, self.leftmost_char,
                          otherstring)
            screen.chgat(self.topmost_char, self.leftmost_char,
                         self.total_chars_x, curses.color_pair(1)
                         | curses.A_UNDERLINE | curses.A_BOLD)
        except curses.error:
            pass

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

        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_YELLOW)  # id 1
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
        curses.endwin()  # NOTE: Still not sure about the persistance of screen

    def show_curses_representation(self, otherstring=None):
        curses.wrapper(self._display_string_rep_using_curses, otherstring)

    def show_on_screen(self, screen, string):
        self._display_string_using_curses(screen, string)

    def add_to_screen(self, screen, string):
        """Same as above but does not refresh"""
        self._add_string_using_curses(screen, string)


def key_press_and_print_df(stdscr, df):
    curses.curs_set(0)
    # stdscr = curses.initscr()
    stdscr.clear()
    viewing_area = ViewingArea(8, 2)
    df_window = DFWindow(df, viewing_area)

    df_window.add_data_to_screen(stdscr)
    stdscr.addstr(0, 0, df_window.get_location_string())
    stdscr.refresh()

    key = -1
    # The scroller loop
    while key not in [ENTER, QUIT]:
        key = stdscr.getch()
        # Movement based on vim keys
        if key in [SCROLL_LEFT, curses.KEY_LEFT]:
            df_window.move_left()
        elif key in [SCROLL_RIGHT, curses.KEY_RIGHT]:
            df_window.move_right()
        elif key in [SCROLL_DOWN, curses.KEY_DOWN]:
            df_window.move_down()
        elif key in [SCROLL_UP, curses.KEY_UP]:
            df_window.move_up()
        # Moving fast
        elif key == PAGE_DOWN:
            df_window.page_down()
        elif key == PAGE_UP:
            df_window.page_up()
        elif key == curses.KEY_RESIZE:
            print("Terminal resized. Please restart the scroller")
            break

        stdscr.clear()
        df_window.add_data_to_screen(stdscr)
        stdscr.addstr(0, 0, df_window.get_location_string())
        stdscr.refresh()

    stdscr.clear()
    stdscr.refresh()
    curses.endwin()


def scroll(scrollable):
    if isinstance(scrollable, pd.core.frame.DataFrame):
        curses.wrapper(key_press_and_print_df, scrollable)
    else:
        print('type ' + str(type(scrollable)) + ' not yet scrollable!')


def scroll_csv(csv_path,
               sep,
               encoding):

    pandas_df = pd.read_csv(csv_path,
                            dtype=object,
                            sep=sep,
                            encoding=encoding)
    scroll(pandas_df)


def main():
    scroll_csv(sys.argv[1])


if __name__ == '__main__':
    main()
