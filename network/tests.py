from django.test import TestCase
from . import models

User = models.User

# Create your tests here.
class TestRegister(TestCase):
    def setUp(self):
        user = User.objects.create_user("spielmeister", "ianspeelman@gmail.com", "wajogino")
        user.save()
    
    def test_user_existence(self):
        ian = User.objects.get(email="ianspeelman@gmail.com")
        self.assertEqual(ian.email, "ianspeelman@gmail.com")