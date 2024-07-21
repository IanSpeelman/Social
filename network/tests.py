from django.test import TestCase, Client
from . import models
import time

User = models.User
c = Client()

# Create your tests here.
class TestRegister(TestCase):
    def setUp(self):
        c.post("/register", {"username": "meister", "email": "ianspeelman@gmail.com", "password":"wajogino", "confirmation": "wajogino"})
    
    def test_user_existence(self):
        user = User.objects.get(username="meister")
        self.assertEqual(user.username, "meister")