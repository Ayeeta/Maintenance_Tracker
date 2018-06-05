import unittest
from user import User

class USERTESTS(unittest.TestCase):
    
    def setUp(self):
        self.usr = User()

    def test_login_user_method(self):
        result = self.usr.login('CF123','pwd123')
        self.assertIsInstance(result, tuple)