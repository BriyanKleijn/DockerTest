import unittest

# For information about running tests see testplan


class TestTemplate(unittest.TestCase):
    def setUp(self):
        self.variable = "Initialize variables"

    def test_1(self):
        # Arrange
        a = 1
        b = 1
        expected = 2

        # Act
        actual = a + b

        # Assert
        self.assertEqual(expected, actual)

    def test_2(self):
        # Arrange
        a = 2
        b = 1
        expected = 1

        # Act
        actual = a - b

        # Assert
        self.assertEqual(expected, actual)

    def tearDown(self):
        self.variable = "Delete/change variables if neccesary"


def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestTemplate('test_1'))
    suite.addTest(TestTemplate('test_2'))
    return suite


if __name__ == '__main__':
    unittest.main()
