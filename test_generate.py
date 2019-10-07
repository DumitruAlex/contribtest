import generate
import unittest

class GenerateTest(unittest.TestCase):

    def test_empty_file(self):
        with open('some_empty_file.rst', 'w') as f:
            f.write('{}')

        expected = ({}, '')
        result = generate.read_file('some_empty_file.rst')

        self.assertEqual(result[0], expected[0])
        self.assertEqual(result[1], expected[1])


    def test_list(self):
        expected = [('test/source/contact.rst', 'contact'),
                    ('test/source/index.rst', 'index')]
        result = [file for file in generate.list_files('test/source')]
        nr_result = len(result)

        self.assertEqual(nr_result, 2)
        self.assertEqual(result, expected)


    def test_correct_read(self):
        expected = ({"title": "My awesome site", "layout": "home.html"},
                    "blah blah")
        result = generate.read_file('test/source/index.rst')

        self.assertEqual(result, expected)


    def test_incorrect_file_format(self):
        with open('test/source/incorrect_file.txt', 'w') as f:
            f.write('{}')

        expected = [('test/source/contact.rst', 'contact'),
                    ('test/source/index.rst', 'index')]
        result = [file for file in generate.list_files('test/source')]

        self.assertEqual(result, expected)