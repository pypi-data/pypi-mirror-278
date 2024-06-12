import unittest
from src.code_ import *

class TestCode(unittest.TestCase):

    def test_get_code(self):
        with open("tests/ressources/outils/remove_comments_with.nf", 'r') as f:
            code_with_comments = f.read()

        with open("tests/ressources/outils/remove_comments_wo.nf", 'r') as f:
            code_wo_comments = f.read()
        code = Code(code_with_comments, origin=None)
        self.assertEqual(code.code, '\n'+code_with_comments+'\n')
        self.assertEqual(code.code_wo_comments.strip(), code_wo_comments.strip())
        self.assertEqual(code.get_code(), code_wo_comments.strip())
    
