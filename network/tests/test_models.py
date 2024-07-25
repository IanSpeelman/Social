from django.test import TestCase, Client

from network.models import User, Post, Follow, Likes

class test_models(TestCase):
    def setUp(self):
        client = Client()
        self.user = User.objects.create_user(username="testuser", password="password", email="testemail@gmail.com")
        self.user2 = User.objects.create_user(username="testuser2", password="password", email="testemail@gmail.com")
        client.login(username="testuser", password="password")
        pass
    
    def test_create_post(self):
        Post.objects.create(user=self.user, content="this is a post")
        post = Post.objects.all().latest("id")
        self.assertEqual(post.content, "this is a post")
        pass

    def test_following_user(self):
        Follow.objects.create(followed=self.user2, follower=self.user)
        follow = Follow.objects.all().latest("id")

        self.assertEqual(follow.follower, self.user)
        self.assertEqual(follow.followed, self.user2)

    def test_liking_post(self):
        Post.objects.create(user=self.user, content="this is a post")
        last_post = Post.objects.all().latest("id")
        Likes.objects.create(user=self.user, post=last_post)
        likes = Likes.objects.all().latest("id")

        self.assertEqual(likes.user, self.user)
        self.assertEqual(likes.post, last_post)

