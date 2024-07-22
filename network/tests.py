from django.test import TestCase, Client
from . import models
import time
from random import random
import math

User = models.User
Post = models.Post
c = Client()

# Create your tests here.
class TestRegister(TestCase):
    def setUp(self):
        c.post("/register", {"username": "meister", "email": "ianspeelman@hotmail.com", "password":"wajogino", "confirmation": "wajogino"})

    def test_user_existence(self):
        user = User.objects.get(username="meister")
        self.assertEqual(user.username, "meister")

class TestPost(TestCase):
    def setUp(self):
        c.post("/register", {"username": "meister", "email": "ianspeelman@hotmail.com", "password":"wajogino", "confirmation": "wajogino"})
        c.login(username="spielmeister", password="wajogino")

    def test_post_creation(self):
        c.post("/", {"body":"this is the body"})
        post = Post.objects.get(user=1)
        self.assertEqual(post.content, "this is the body")

    def test_listing_all_posts(self):
        n = math.floor(random() * 100)
        for i in range(n):
            c.post("/", {"body": f"this is post ${i}"})
        list = Post.objects.all()
        self.assertEqual(len(list), n)