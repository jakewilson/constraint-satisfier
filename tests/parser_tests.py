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

    @classmethod
    def tearDownClass(self):
        name = self.f.name
        self.f.close()
        os.remove(name)

    def test_tokenizer_1(self):
        self.write('NT != SA')
        self.assertEqual((parser.Token.ID, 'NT'), parser.get_token(self.f))
        self.assertEqual((parser.Token.NOT_EQUAL,), parser.get_token(self.f))
        self.assertEqual((parser.Token.ID, 'SA'), parser.get_token(self.f))

    def test_tokenizer_2(self):
        self.write('V = 25')
        self.assertEqual((parser.Token.ID, 'V'), parser.get_token(self.f))
        self.assertEqual((parser.Token.EQUAL,), parser.get_token(self.f))
        self.assertEqual((parser.Token.NUM, 25), parser.get_token(self.f))

    def test_tokenizer_3(self):
        self.write('var1')
        self.assertEqual((parser.Token.ID, 'var1'), parser.get_token(self.f))

    def test_tokenizer_4(self):
        self.write('= = !=           26 == 78')
        self.assertEqual((parser.Token.EQUAL,), parser.get_token(self.f))
        self.assertEqual((parser.Token.EQUAL,), parser.get_token(self.f))
        self.assertEqual((parser.Token.NOT_EQUAL,), parser.get_token(self.f))
        self.assertEqual((parser.Token.NUM, 26), parser.get_token(self.f))
        self.assertEqual((parser.Token.EQUAL,), parser.get_token(self.f))
        self.assertEqual((parser.Token.EQUAL,), parser.get_token(self.f))
        self.assertEqual((parser.Token.NUM, 78), parser.get_token(self.f))

    def test_tokenizer_5(self):
        self.write('nsw != \'blue\'')
        self.assertEqual((parser.Token.ID, 'nsw'), parser.get_token(self.f))
        self.assertEqual((parser.Token.NOT_EQUAL,), parser.get_token(self.f))
        self.assertEqual((parser.Token.STRING, 'blue'), parser.get_token(self.f))

    def test_tokenizer_6(self):
        self.write('var ! \'red\'') # forgot '=' after '!'
        self.assertEqual((parser.Token.ID, 'var'), parser.get_token(self.f))
        self.assertEqual((parser.Token.ERROR,), parser.get_token(self.f))

    def write(self, s):
        self.f.seek(0, 0)
        self.f.truncate() # remove file contents
        self.f.write(s)
        self.f.seek(0, 0)
        

if __name__ == '__main__':
    unittest.main()
