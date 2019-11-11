from django.shortcuts import reverse
from django.test import TestCase, Client
from .models import BlogPost


class BlogPostPage(TestCase):
    def setUp(self):
        for item in range(12):
            BlogPost.objects.get_or_create(
                title=f'test {item}', description=f'description {item}')

    def test_user_can_see_list_of_posts(self):
        response = self.client.get(reverse('blog:list'))
        self.assertContains(response, 'Test', 10)
        self.assertContains(response, 'description', 10)

    def test_user_can_see_post_detail(self):
        response = self.client.get(
            reverse('blog:detail', kwargs={'slug': 'test-1'}))
        self.assertContains(response, 'Test')
