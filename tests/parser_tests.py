import unittest
import os

import sys
sys.path.insert(0, os.path.abspath('.'))

import parser

class TestParser(unittest.TestCase):

    PATH = 'parser_test'

    @classmethod
    def setUpClass(self):
        self.f = open(TestParser.PATH, 'a+')
        self.parser = parser.Parser()

    @classmethod
    def tearDownClass(self):
        name = self.f.name
        self.f.close()
        os.remove(name)

    def test_tokenizer_1(self):
        self.write('NT != SA')
        self.assertEqual((parser.Token.ID, 'NT'), self.parser.get_token(self.f))
        self.assertEqual((parser.Token.NOT_EQUAL,), self.parser.get_token(self.f))
        self.assertEqual((parser.Token.ID, 'SA'), self.parser.get_token(self.f))

    def test_tokenizer_2(self):
        self.write('V = 25')
        self.assertEqual((parser.Token.ID, 'V'), self.parser.get_token(self.f))
        self.assertEqual((parser.Token.EQUAL,), self.parser.get_token(self.f))
        self.assertEqual((parser.Token.NUM, 25), self.parser.get_token(self.f))

    def test_tokenizer_3(self):
        self.write('var1')
        self.assertEqual((parser.Token.ID, 'var1'), self.parser.get_token(self.f))

    def test_tokenizer_4(self):
        self.write('= = !=           26 == 78')
        self.assertEqual((parser.Token.EQUAL,), self.parser.get_token(self.f))
        self.assertEqual((parser.Token.EQUAL,), self.parser.get_token(self.f))
        self.assertEqual((parser.Token.NOT_EQUAL,), self.parser.get_token(self.f))
        self.assertEqual((parser.Token.NUM, 26), self.parser.get_token(self.f))
        self.assertEqual((parser.Token.EQUAL,), self.parser.get_token(self.f))
        self.assertEqual((parser.Token.EQUAL,), self.parser.get_token(self.f))
        self.assertEqual((parser.Token.NUM, 78), self.parser.get_token(self.f))

    def test_tokenizer_5(self):
        self.write('nsw != \'blue\'')
        self.assertEqual((parser.Token.ID, 'nsw'), self.parser.get_token(self.f))
        self.assertEqual((parser.Token.NOT_EQUAL,), self.parser.get_token(self.f))
        self.assertEqual((parser.Token.STRING, 'blue'), self.parser.get_token(self.f))

    def test_tokenizer_6(self):
        self.write('var ! \'red\'') # forgot '=' after '!'
        self.assertEqual((parser.Token.ID, 'var'), self.parser.get_token(self.f))
        self.assertEqual((parser.Token.ERROR,), self.parser.get_token(self.f))

    def test_tokenizer_6(self):
        self.write('var = sa')
        self.assertEqual((parser.Token.ID, 'var'), self.parser.get_token(self.f))
        self.assertEqual((parser.Token.EQUAL,), self.parser.get_token(self.f))
        self.assertEqual((parser.Token.ID, 'sa'), self.parser.get_token(self.f))

    def test_tokenizer_7(self):
        self.write('var=sa')
        self.assertEqual((parser.Token.ID, 'var'), self.parser.get_token(self.f))
        self.assertEqual((parser.Token.EQUAL,), self.parser.get_token(self.f))
        self.assertEqual((parser.Token.ID, 'sa'), self.parser.get_token(self.f))

    def test_is_letter(self):
        for c in xrange(ord('A'), ord('Z')):
            self.assertEqual(parser.is_letter(chr(c)), True)
        for c in xrange(ord('a'), ord('z')):
            self.assertEqual(parser.is_letter(chr(c)), True)

        # test off by one errors
        self.assertEqual(parser.is_letter(chr(ord('A') - 1)), False)
        self.assertEqual(parser.is_letter(chr(ord('Z') + 1)), False)
        self.assertEqual(parser.is_letter(chr(ord('a') - 1)), False)
        self.assertEqual(parser.is_letter(chr(ord('z') + 1)), False)

    def test_is_digit(self):
        for c in xrange(ord('0'), ord('9')):
            self.assertEqual(parser.is_digit(chr(c)), True)

        self.assertEqual(parser.is_digit(chr(ord('0') - 1)), False)
        self.assertEqual(parser.is_digit(chr(ord('9') + 1)), False)

    def test_parser_1(self):
        self.write('var = sabby')
        desc = self.parser.parse(self.f)
        self.compareLists(desc[0], ['var', 'sabby'])
        self.assertEqual(desc[1]({'var': 1, 'sabby': 1}), True)
        self.assertEqual(desc[1]({'var': 2, 'sabby': 1}), False)

    def test_parser_2(self):
        self.write('var == sa')
        with self.assertRaises(SyntaxError):
            self.parser.parse(self.f)

    def test_parser_3(self):
        self.write('25 = SA')
        with self.assertRaises(SyntaxError):
            self.parser.parse(self.f)

    def test_parser_4(self):
        self.write("variable = 'blue'")
        desc = self.parser.parse(self.f)
        self.compareLists(desc[0], ['variable'])

    def test_parser_5(self):
        self.write("variable = 'blue'\nanothervar != thirdone")
        desc = self.parser.parse(self.f)
        self.compareLists(desc[0], ['variable', 'anothervar', 'thirdone'])

    def test_parser_6(self):
        self.write("variable = 'blue'\nanothervar")
        with self.assertRaises(SyntaxError):
            self.parser.parse(self.f)

    def test_parser_7(self):
        self.write('var = 89')
        desc = self.parser.parse(self.f)
        self.compareLists(desc[0], ['var'])

    def write(self, s):
        self.f.seek(0, 0)
        self.f.truncate() # remove file contents
        self.f.write(s)
        self.f.seek(0, 0)

    def compareLists(self, ret, l):
        for name in l:
            self.assertEqual(name in ret, True)

if __name__ == '__main__':
    unittest.main()
