import os
import sys
import io
import unittest

from datascroller.scroller import ViewingArea


class TestViewingArea(unittest.TestCase):

    def test_padding(self):
        """Grabbing the output of print_representation"""
        stdout = sys.stdout
        sys.stdout = io.StringIO()

        va = ViewingArea(4, 2)
        va.print_representation()
        output = sys.stdout.getvalue()

        sys.stdout = stdout

        rows = [r for r in output.split('\n') if r != '']
        max_x, max_y = va.get_terminal_size()

        self.assertEqual(max_y, len(rows))
        self.assertEqual(max_x, len(rows[0]))

        self.assertEqual(set(rows[0]), {'P'})
        self.assertEqual(set(rows[1]), {'P'})

        self.assertEqual(rows[2][:5], 'PPPPX')

if __name__ == '__main__':
    unittest.main()
