import unittest

from packet_drop.packet_drop import update_average


# class TestAverage(unittest.TestCase):
#     def test_value(self):
#         """
#         Check that the function actually averages numbers correctly
#         """
#         self.assertEqual(average([10.000, 19.53]), 14.77)
#         self.assertEqual(average([10.0, 20.0]), 15.0)
#         self.assertNotEqual(average([2, 6]), 9)

#     def test_float(self):
#         """
#         Return type is float
#         """
#         self.assertTrue(isinstance(average([10.000, 19.53]), float))


class TestUpdateAverage(unittest.TestCase):
    def test_value(self):
        """
        Check that the updated dict value is correct
        """
        averages = {'min': [],
                    'avg': [],
                    'max': [],
                    'mdev': [],
                    }
        self.assertEqual(update_average(averages, 'min', 10.00), 10.00)
        self.assertEqual(update_average(averages, 'min', 5.00), 7.50)
        self.assertEqual(update_average(averages, 'min', 7.86), 7.62)

        self.assertEqual(update_average(averages, 'avg', 5.78), 5.78)
        self.assertEqual(update_average(averages, 'avg', 12.73), 9.26)

        self.assertEqual(update_average(averages, 'min', 1.23), 6.02)

        self.assertEqual(len(averages['max']), 0)
        self.assertEqual(len(averages['mdev']), 0)

if __name__ == '__main__':
    unittest.main()
