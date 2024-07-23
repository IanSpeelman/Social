from django.test import TestCase, Client

from network.models import User, Post

class test_models(TestCase):
    def setUp(self):
        client = Client()
        self.user = User.objects.create_user(username="testuser", password="password", email="testemail@gmail.com")
        client.login(username="testuser", password="password")
        pass
    
    def test_create_post(self):
        Post.objects.create(user=self.user, content="this is a post")
        post = Post.objects.all().latest("id")
        self.assertEqual(post.content, "this is a post")
        pass