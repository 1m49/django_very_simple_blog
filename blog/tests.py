from django.test import TestCase
from django.contrib.auth.models import User
from .models import Post
from django.shortcuts import reverse


class BlogPostTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='iman1')
        cls.post1 = Post.objects.create(
            title='post1',
            text='this is just for test',
            author=cls.user,
            status='pub',
            # status=Post.STATUS_CHOICES[0][0],
        )

        cls.post2 = Post.objects.create(
            title='post2',
            text='this is just 2',
            author=cls.user,
            status='drf',
            # status=Post.STATUS_CHOICES[1][0]
        )

    # show post list by url
    def test_post_list_by_url(self):
        response = self.client.get('')
        self.assertURLEqual(response.status_code, 200)

    # show post list page by name
    def test_post_list_by_name(self):
        response = self.client.get(reverse('all_posts'))
        self.assertURLEqual(response.status_code, 200)

    # show title in posts list
    def test_post_title_on_blog_list_page(self):
        response = self.client.get(reverse('all_posts'))
        self.assertContains(response, self.post1.title)

    # show detail page
    def test_post_detail_on_blog_detail_page(self):
        response = self.client.get(f'/{self.post1.id}/')
        self.assertContains(response, self.post1.title)
        self.assertContains(response, self.post1.text)
        self.assertContains(response, self.post1.author)

    # post detail by url
    def test_post_detail_by_url(self):
        response = self.client.get(f'/{self.post1.id}/')
        self.assertEqual(response.status_code, 200)

    # post detail by name
    def test_post_detail_by_name(self):
        response = self.client.get(reverse('post_detail', args=[self.post1.id]))
        self.assertEqual(response.status_code, 200)

    # Error 404 should work properly
    def test_status_404_if_post_does_not_exists(self):
        response = self.client.get(reverse('post_detail', args=[9999]))
        self.assertEqual(response.status_code, 404)

    # Draft posts should not be displayed
    def test_draft_post_not_show_on_post_list_page(self):
        response = self.client.get(reverse('all_posts'))
        self.assertContains(response, self.post1.title)
        self.assertNotContains(response, self.post2.title)

    # test for create post
    def test_post_create_view(self):
        response = self.client.post(reverse('post_create'), {
            'title': 'hello my name is iman akbari',
            'text': 'i love django',
            'status': 'pub',
            'author': self.user.id,
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.last().title, 'hello my name is iman akbari')
        self.assertEqual(Post.objects.last().text, 'i love django')

    # test for post detail
    def test_post_update_view(self):
        response = self.client.post(reverse('post_update', args=[self.post2.id]), {
            'title': 'post2 updated',
            'text': 'this is just test for post2',
            'status': 'pub',
            'author': self.post2.author.id,
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.last().title, 'post2 updated')
        self.assertEqual(Post.objects.last().text, 'this is just test for post2')

    # test for delete post
    def test_post_delete_view(self):
        response = self.client.post(reverse('post_delete', args=[self.post2.id]))
        self.assertEqual(response.status_code, 302)
