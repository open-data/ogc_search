from django.test import TestCase
from search_util import calc_starting_row
# Create your tests here.


class UtilTestCase(TestCase):

    def test_calc_starting_row(self):
        start_page = calc_starting_row(34, 10)
        self.assertEqual(start_page[0], 330)
