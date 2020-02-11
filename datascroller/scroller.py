import sys
import shutil
import curses
import time
import pandas as pd
from pandasql import sqldf
from datascroller import help_screen as help
from datascroller import keybindings as keys


class DFWindow:
    """The data frame window"""

    def __init__(self, pandas_df, viewing_area, reader=None):
        self.full_df = pandas_df
        (self.total_rows, self.total_cols) = pandas_df.shape

        self.viewing_area = viewing_area
        self.reader = reader

        self.rows_to_print = (self.viewing_area.bottommost_char -
                              self.viewing_area.topmost_char + 1)

        self.highlight_mode = False
        self.highlight_row = 0

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

    def update_viewing_area(self, viewing_area):
        """Update viewing area. Useful if terminal is resized while
        user is viewing a subset of the original dataframe"""
        self.viewing_area = viewing_area

        self.rows_to_print = (self.viewing_area.bottommost_char -
                              self.viewing_area.topmost_char + 1)

        # update current view before accepting new input
        self.update_dataframe_coords(self.r_1, self.c_1)

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

        NOTE: This method might still prove useful if single-cell highlighting
        is implemented
        """

        positions = []
        for j in range(1, self.total_cols + 1):
            row_str = self.full_df.iloc[self.r_1:self.r_2, 0:j].to_string().split('\n')[self.highlight_row]
            positions.append([len(row_str) - len(str(self.full_df.iloc[self.highlight_row, j - 1])), len(row_str)])
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
        move_window = True
        if self.highlight_mode:
            # try to move highlight, otherwise move window
            move_window = self.highlight_row == self.rows_to_print - 1
            if not move_window:
                self.viewing_area.move_highlight_down()
                self.highlight_row += 1

        if move_window and self.r_2 < self.full_df.shape[0]:
            self.update_dataframe_coords(start_row=self.r_1 + 1,
                                         start_col=self.c_1)

    def move_up(self):
        move_window = True
        if self.highlight_mode:
            # try to move highlight, otherwise move window
            move_window = self.highlight_row == 0
            if not move_window:
                self.viewing_area.move_highlight_up()
                self.highlight_row -= 1

        if move_window and self.r_1 > 0:
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

    def toggle_highlight_mode(self):
        self.highlight_mode = not self.highlight_mode
        self.viewing_area.toggle_highlight_mode()

    def line_search(self, line):
        new_start_row = 0
        if line <= 0:
            # go to top
            pass
        elif line >= self.full_df.shape[0] - self.rows_to_print:
            # go to bottom
            new_start_row = self.full_df.shape[0] - self.rows_to_print
        else:
            new_start_row = line

        self.update_dataframe_coords(start_row=new_start_row,
                                     start_col=self.c_1)

    def filter(self, query_string, viewing_area):
        raw_cols = query_string.split(",")
        cleaned_cols = [col.strip() for col in raw_cols]
        return DFWindow(self.full_df.filter(items=cleaned_cols), viewing_area)

    def query(self, query_string, viewing_area):
        df = self.full_df
        return DFWindow(sqldf(query_string, locals()), viewing_area)

        # in progress
        # this rigamarole means the user can use any table name they want
        #    query_words = query_string.lower().split()
        #    from_index = query_words.index("from")
        #    table_name = query_words[from_index + 1]
        #    exec("%s = %d" % (table_name, self.full_df))

    def get_next_chunk(self):
        try:
            df = self.reader.get_chunk()
        # if we reach the last chunk, just stop there
        except StopIteration:
            df = self.full_df
        return DFWindow(df, self.viewing_area, self.reader)


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

        self.highlight_mode = False
        self.highlight_row = 0

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

    def get_terminal_size(self):
        return self.total_chars_x, self.total_chars_y

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
            if self.highlight_mode:
                screen.chgat(self.topmost_char + 1 + self.highlight_row, self.pad_chars_x,
                             self.rightmost_char, curses.A_STANDOUT)
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

    def toggle_highlight_mode(self):
        self.highlight_mode = not self.highlight_mode

    # NOTE(johncmerfeld): for single-cell highlighting -- do not use yet
    def move_highlight_left(self):
        self.highlight_col -= 1
    # NOTE(johncmerfeld): for single-cell highlighting -- do not use yet

    def move_highlight_right(self):
        self.highlight_col += 1

    def move_highlight_down(self):
        self.highlight_row += 1

    def move_highlight_up(self):
        self.highlight_row -= 1


def add_help_string(screen, cols):
    screen.addstr(0, 0, help.BANNER, curses.A_BOLD)
    screen.chgat(0, 0, cols, curses.A_UNDERLINE)
    for i, option in enumerate(help.MENU_OPTIONS):
        exec("screen.addstr(i + 1, 1, help." + option + ", curses.A_BOLD)")
        exec("screen.addstr(i + 1, cols - 1 - len(help." + option + "_TEXT), help." + option + "_TEXT)")


def show_help_view(screen, cols, rows):

    width = help.HELP_BOX_WIDTH
    height = len(help.MENU_OPTIONS) + 3
    box1 = screen.subwin(height, width, 1, cols - width)
    box2 = screen.subwin(height - 2, width - 2, 2, cols - width + 1)
    box1.immedok(True)  # updates automatically
    box2.immedok(True)
    box1.erase()  # clears text
    box1.box()  # adds border
    add_help_string(box2, width - 2)


def get_user_input_with_prompt(stdscr, row, col, prompt):
    curses.echo()
    stdscr.addstr(row, col, prompt)
    stdscr.refresh()
    curses.curs_set(1)
    input = stdscr.getstr(row, col + len(prompt))
    curses.curs_set(0)
    return input  # ^^^^  reading input at next column


def print_user_alert(stdscr, alert):
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    stdscr.addstr(0, 30, alert)
    stdscr.chgat(0, 30, len(alert), curses.A_BOLD | curses.color_pair(2))


def print_user_error(stdscr, error):
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
    stdscr.addstr(0, 30, "Error: " + error)
    stdscr.chgat(0, 30, len("Error: " + error), curses.A_BOLD | curses.color_pair(3))


def key_press_and_print_df(stdscr, df, reader=None):
    curses.curs_set(0)
    # stdscr = curses.initscr()
    stdscr.clear()
    viewing_area = ViewingArea(8, 2)
    term_cols, term_rows = viewing_area.get_terminal_size()
    df_window = DFWindow(df, viewing_area, reader)

    df_window.add_data_to_screen(stdscr)

    help_view = False
    err_string = ""
    stdscr.addstr(0, 0, df_window.get_location_string())

    # On first open only, add hint for help menu
    # NOTE: could leave it up, also.
    print_user_alert(stdscr, "Press ' (single quote) for help menu")
    stdscr.refresh()

    key = keys.NULL_KEY
    # The scroller loop
    while key not in [keys.ENTER, keys.QUIT]:
        err_string = ""
        key = stdscr.getch()
        # Movement based on vim keys
        if key in [keys.SCROLL_LEFT, curses.KEY_LEFT]:
            df_window.move_left()
        elif key in [keys.SCROLL_RIGHT, curses.KEY_RIGHT]:
            df_window.move_right()
        elif key in [keys.SCROLL_DOWN, curses.KEY_DOWN]:
            df_window.move_down()
        elif key in [keys.SCROLL_UP, curses.KEY_UP]:
            df_window.move_up()

        # Moving fast
        elif key == keys.PAGE_DOWN:
            df_window.page_down()
        elif key == keys.PAGE_UP:
            df_window.page_up()

        # alternate views
        elif key == keys.HIGHLIGHT:
            df_window.toggle_highlight_mode()

        elif key == keys.HELP:
            help_view = not help_view

        # search functionality
        elif key == keys.LINE_SEARCH:
            search_string = get_user_input_with_prompt(stdscr, term_rows - 1, 0,
                                                       "Goto line: ")
            if len(search_string) > 0:
                try:
                    df_window.line_search(int(search_string))
                except ValueError:
                    err_string = "Please enter a valid (integer) line number"

        elif key == keys.FILTER:
            query_bytes = get_user_input_with_prompt(stdscr, term_rows - 1, 0,
                                                     "Column filter: ")
            query_string = query_bytes.decode(encoding="utf-8")
            if len(query_string) > 0:
                df_window = df_window.filter(query_string, viewing_area)
                # NOTE: if column names are invalid,
                # an empty dataframe is returned.
                # We could preempt this if we wanted.

        elif key == keys.QUERY:
            query_bytes = get_user_input_with_prompt(stdscr, term_rows - 1, 0,
                                                     "SQL query (use 'df' as table name): ")
            query_string = query_bytes.decode(encoding="utf-8")
            if len(query_string) > 0:
                try:
                    df_window = df_window.query(query_string, viewing_area)
                except:  # noqa: E722
                    err_string = "Syntax error in query"
                    # TODO(johncmerfeld): be more specific with this error

        elif key == keys.BACK:
            # exit query mode, essentially
            df_window = DFWindow(df, viewing_area)

        elif key == curses.KEY_RESIZE:
            viewing_area = ViewingArea(8, 2)
            term_cols, term_rows = viewing_area.get_terminal_size()
            df_window.update_viewing_area(viewing_area)
            df_window.add_data_to_screen(stdscr)

        elif reader is not None and key == keys.NEXT_CHUNK:
            df_window = df_window.get_next_chunk()

        stdscr.clear()
        df_window.add_data_to_screen(stdscr)
        stdscr.addstr(0, 0, df_window.get_location_string())

        if help_view:
            show_help_view(stdscr, term_cols, term_rows)

        if err_string:
            print_user_error(stdscr, err_string)

        stdscr.refresh()

    stdscr.clear()
    stdscr.refresh()
    curses.endwin()


def scroll(df_or_reader):
    if isinstance(df_or_reader, pd.core.frame.DataFrame):
        curses.wrapper(key_press_and_print_df, df_or_reader)
    elif isinstance(df_or_reader, pd.io.parsers.TextFileReader):
        first_chunk = df_or_reader.get_chunk()
        curses.wrapper(key_press_and_print_df, first_chunk, df_or_reader)
    else:
        print('type ' + str(type(df_or_reader)) + ' not yet scrollable!')


def scroll_csv(csv_path, sep, encoding, nrows, chunksize):
    df_or_reader = pd.read_csv(csv_path,
                               dtype=object,
                               sep=sep,
                               encoding=encoding,
                               nrows=nrows,
                               chunksize=chunksize)
    scroll(df_or_reader)


def main():
    scroll_csv(sys.argv[1])


if __name__ == '__main__':
    main()
