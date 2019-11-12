from django.shortcuts import reverse
from django.test import TestCase, Client
from .models import Coach


class BlogPostPage(TestCase):
    def setUp(self):
        for item in range(6):
            Coach.objects.get_or_create(
                name=f'Name {item}', email=f'name{item}@gmail.com', phone='1(651)000-00-00')

    def test_user_can_see_coaches(self):
        response = self.client.get(reverse('club:main'))

        self.assertContains(response, 'Name 1', 1)
