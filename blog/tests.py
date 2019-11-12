from django.shortcuts import reverse
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.utils import timezone
from .models import BlogPost


class BlogPostPage(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            'testuser', 'testuser@gmail.com', 'testpass')
        for item in range(12):
            BlogPost.objects.get_or_create(
                title=f'test title {item}', description=f'description {item}', author=self.user, published=True)

    def test_user_can_see_list_of_published_posts(self):
        response = self.client.get(reverse('blog:list'))
        # including title in the link
        self.assertContains(response, 'Test Title', 20)
        self.assertContains(response, 'description', 10)

    def test_user_cannot_see_unpublished_posts(self):
        BlogPost.objects.get_or_create(
            title='unpublished title', description='description', author=self.user, published=False)

        response_list = self.client.get(
            f"{reverse('blog:list')}?page=2")
        self.assertNotContains(response_list, 'Unpublished Title')

        response_detail = self.client.get(
            reverse('blog:detail', kwargs={'slug': 'unpublished-title'}))
        self.assertTrue(response_detail.status_code, 404)

    def test_user_can_see_post_detail(self):
        response = self.client.get(
            reverse('blog:detail', kwargs={'slug': 'test-title-1'}))
        self.assertContains(response, 'Test')

    def test_post_contains_published_date(self):
        response = self.client.get(
            reverse('blog:detail', kwargs={'slug': 'test-title-1'}))
        self.assertContains(response, timezone.now().strftime('%b %d %Y'))

    def test_list_of_post_contains_pagination(self):
        response = self.client.get(reverse('blog:list'))

        self.assertContains(response, 'Page 1 out of 2')
