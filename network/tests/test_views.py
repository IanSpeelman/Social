from django.contrib.auth import login, logout
from django.urls import reverse
from django.test import TestCase, Client
from django.db import IntegrityError, transaction

from network.models import User, Post, Follow, Likes

class test_models(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="password", email="testemail@gmail.com")
        self.client.login(username="testuser", password="password")

        # urls
        self.index_url = reverse("index")
        self.login_url = reverse("login")
        self.register_url = reverse("register")
        self.logout_url = reverse("logout")
        self.follow_url = reverse("followed")

    def test_index_GET_no_page(self):
        response = self.client.get(self.index_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("/network/index.html")

    def test_index_GET_page_to_high(self):
        response = self.client.get(f"{self.index_url}/?page=12")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("/network/index.html")

    def test_index_GET_page_to_low(self):
        response = self.client.get(f"{self.index_url}?page=-12")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("/network/index.html")

    def test_index_GET_page_no_integer(self):
        response = self.client.get(f"{self.index_url}?page=sdf")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("/network/index.html")

    def test_login_GET(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("/network/login.html")

    def test_register_GET(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("/network/register.html")

    def test_logout_GET(self):
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)
        
    def test_index_POST(self):
        body = "this is a new post"
        response = self.client.post(self.index_url, {
            "body": body,
        })
        latest = Post.objects.all().latest("id")
        self.assertEqual(latest.content, body)
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed("/network/index.html")

    def test_login_POST(self):
        self.client.logout()
        response = self.client.post(self.login_url, {
            "username": "testuser",
            "password": "password",
        })
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed("/network/index.html")

    def test_register_POST(self):
        response = self.client.post(self.register_url, {
            "username": "testuser2",
            "email": "test@email.com",
            "password": "password",
            "confirmation": "password",
        })
        newuser = User.objects.all().latest("id")
        self.assertEqual(newuser.username, "testuser2")
        self.assertEqual(newuser.email, "test@email.com")
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed("/network/register.html")

    def test_index_POST_inclomplete_data(self):
        response = self.client.post(self.index_url)
        self.assertEqual(Post.objects.count(), 0)
        self.assertEqual(response.status_code, 406)
        self.assertTemplateUsed("/network/index.html")

    def test_index_POST_not_logged_in(self):
        self.client.logout()
        body = "this is a new post"
        response = self.client.post(self.index_url, {
            "body": body,
        })
        self.assertEqual(Post.objects.count(), 0)
        self.assertEqual(response.status_code, 406)
        self.assertTemplateUsed("/network/index.html")

    def test_login_POST_inclomplete_data(self):
        self.client.logout()
        response = self.client.post(self.login_url, {
            "username": "",
            "password": "password",
        })
        self.assertEqual(response.status_code, 406)
        self.assertTemplateUsed("/network/login.html")

    def test_login_POST_incorrect_credentials(self):
        self.client.logout()
        response = self.client.post(self.login_url, {
            "username": "this_user_does_not_exist",
            "password": "this_password_makes_no_sense",
        })
        self.assertEqual(response.status_code, 406)
        self.assertTemplateUsed("/network/login.html")

    def test_register_POST_inclomplete_data(self):
        self.client.logout()
        response = self.client.post(self.register_url, {
            "username": "",
            "email": "test@email.com",
            "password": "password",
            "confirmation": "password",
        })
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.status_code, 406)
        self.assertTemplateUsed("/network/register.html")
    
    def test_register_POST_no_match_passwords(self):
        self.client.logout()
        response = self.client.post(self.register_url, {
            "username": "testuser2",
            "email": "test@email.com",
            "password": "password",
            "confirmation": "not_matching",
        })
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.status_code, 406)
        self.assertTemplateUsed("/network/register.html")

    def test_profile_POST(self):
        response = self.client.post(reverse("profile", kwargs={"user_id": 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("/network/profile.html")

    def test_profile_POST_non_existing_user_id(self):
        response = self.client.post(reverse("profile", kwargs={"user_id": 999}))
        self.assertEqual(response.status_code, 302)

    def test_following_profile_GET(self):
        user2  = User.objects.create_user(username="testuser2", password="password", email="testemail@gmail.com")
        response = self.client.get(reverse("follow", kwargs={"user_id":2}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Follow.objects.all().count(), 1)
        response = self.client.get(reverse("follow", kwargs={"user_id":2}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Follow.objects.all().count(), 0)
        self.assertTemplateUsed("/network/profile.html")

    def test_following_profile_GET_not_logged_in(self):
        self.client.logout()
        user2  = User.objects.create_user(username="testuser2", password="password", email="testemail@gmail.com")
        response = self.client.get(reverse("follow", kwargs={"user_id":2}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Follow.objects.all().count(), 0)
        response = self.client.get(reverse("follow", kwargs={"user_id":2}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Follow.objects.all().count(), 0)

    def test_following_page_GET(self):
        response = self.client.get(reverse("followed"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("/network/index.html")

    def test_following_page_GET_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse("followed"))
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed("/network/login.html")

    def test_likes_GET(self):
        newpost = Post(user=self.user, content="this is a test post")
        newpost.save()
        self.assertEqual(Likes.objects.all().count(), 0)
        response = self.client.get(reverse("like", kwargs={"post_id": 1}))
        self.assertEqual(Likes.objects.all().count(), 1)
        self.assertEqual(response.status_code, 200)

    def test_likes_GET_post_does_not_exist(self):
        response = self.client.get(reverse("like", kwargs={"post_id": 1}))
        self.assertEqual(Likes.objects.all().count(), 0)
        self.assertEqual(response.status_code, 404)
        
    def test_likes_GET_user_not_logged_in(self):
        self.client.logout()
        newpost = Post(user=self.user, content="this is a test post")
        newpost.save()
        response = self.client.get(reverse("like", kwargs={"post_id": 1}))
        self.assertEqual(Likes.objects.all().count(), 0)
        self.assertEqual(response.status_code, 401)

    def test_likes_GET_unliking(self):
        newpost = Post(user=self.user, content="this is a test post")
        newpost.save()
        self.assertEqual(Likes.objects.all().count(), 0)
        response = self.client.get(reverse("like", kwargs={"post_id": 1}))
        self.assertEqual(Likes.objects.all().count(), 1)
        response = self.client.get(reverse("like", kwargs={"post_id": 1}))
        self.assertEqual(Likes.objects.all().count(), 0)
        self.assertEqual(response.status_code, 200)

    def test_GET_likes_info(self):
        newpost = Post(user=self.user, content="this is a test post")
        newpost.save()
        response = self.client.get(reverse("postinfo", kwargs={"post_id": 1}))
        self.assertEqual(response.status_code, 200)

    def test_GET_likes_info_post_does_not_exist(self):
        response = self.client.get(reverse("postinfo", kwargs={"post_id": 1}))
        self.assertEqual(response.status_code, 404)

    def test_GET_likes_info_not_logged_in(self):
        self.client.logout()
        newpost = Post(user=self.user, content="this is a test post")
        newpost.save()
        response = self.client.get(reverse("postinfo", kwargs={"post_id": 1}))
        self.assertEqual(response.status_code, 200)