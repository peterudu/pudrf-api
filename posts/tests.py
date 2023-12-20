from django.contrib.auth.models import User
from .models import Post
from rest_framework import status
from rest_framework.test import APITestCase


class PostListViewTests(APITestCase):
    def setUp(self):
        User.objects.create_user(username='prober', password='tester1')

    def test_can_list_posts(self):
        prober = User.objects.get(username='prober')
        Post.objects.create(owner=prober, title='ein titel')
        response = self.client.get('/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        print(len(response.data))

    def test_logged_in_user_can_create_post(self):
        self.client.login(username='prober', password='tester1')
        response = self.client.post('/posts/', {'title': 'ein titel'})
        count = Post.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_not_logged_in_cant_create_post(self):
        response = self.client.post('/posts/', {'title': 'ein titel'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PostDetailViewTests(APITestCase):
    def setUp(self):
        prober = User.objects.create_user(username='prober', password='tester1')
        jan = User.objects.create_user(username='jan', password='tester1')
        Post.objects.create(
            owner=prober, title='ein titel', content='probers content'
        )
        Post.objects.create(
            owner=jan, title='anderer titel', content='jans content'
        )

    def test_can_retrieve_post_using_valid_id(self):
        response = self.client.get('/posts/1/')
        self.assertEqual(response.data['title'], 'ein titel')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cant_retrieve_post_using_invalid_id(self):
        response = self.client.get('/posts/555/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_update_own_post(self):
        self.client.login(username='prober', password='tester1')
        response = self.client.put('/posts/1/', {'title': 'neuer titel'})
        post = Post.objects.filter(pk=1).first()
        self.assertEqual(post.title, 'neuer titel')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cant_update_another_users_post(self):
        self.client.login(username='prober', password='tester1')
        response = self.client.put('/posts/2/', {'title': 'neuer titel'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)