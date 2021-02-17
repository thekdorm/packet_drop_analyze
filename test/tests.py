# Tests could definitely use some work, this is more for practice than anything

import unittest

from packet_drop.packet_drop import update_average, calculate_average


class TestAverages(unittest.TestCase):
    def __init__(self, TestAverages):
        unittest.TestCase.__init__(self, 'test_update_average')
        self.averages = {'per': [],
                         'min': [],
                         'avg': [],
                         'max': [],
                         'mdev': [],
                         }

    def test_update_average(self):
        """
        Check that the averages dictionary is updated correctly

        Note that we are we are testing against self.averages which will
        retain added values to the following tests that use it
        """
        update_average(self.averages, 'per', 10.00)
        update_average(self.averages, 'per', 5.00)
        update_average(self.averages, 'per', 7.86)
        
        update_average(self.averages, 'avg', 5.78)
        update_average(self.averages, 'avg', 12.73)

        update_average(self.averages, 'max', 1.23)

        self.assertEqual([
                          len(self.averages['per']),
                          len(self.averages['avg']),
                          len(self.averages['max']),
                          len(self.averages['min']),
                          len(self.averages['mdev'])
                          ],
                          [3, 2, 1, 0, 0]
                         )
        
        self.assertEqual(calculate_average(self.averages, 'per'), 7.62)
        self.assertEqual(calculate_average(self.averages, 'avg'), 9.26)
        self.assertEqual(calculate_average(self.averages, 'max'), 1.23)

    # def test_calculate_average(self):
    #     """
    #     Check that the average is calculated correctly
    #     
    #     These tests are always passing for some reason when in their own method?
    #     """
    #     self.assertEqual(calculate_average(self.averages, 'per'), 7.62)
    #     self.assertEqual(calculate_average(self.averages, 'avg'), 9.26)
    #     self.assertEqual(calculate_average(self.averages, 'min'), 6.02)


if __name__ == '__main__':
    unittest.main()
