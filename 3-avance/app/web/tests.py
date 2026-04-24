from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Article, UserFavouriteArticle

class ViewsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="toto",
            password="123"
        )
        self.article = Article.objects.create(
            title="123",
            author=self.user,
            synopsis = "qweqwe",
            content="lasdkjf ;aslkdjfl;askjdf"
        )

    def test_favourites_page(self):
        response = self.client.get(reverse("favourites"))
        self.assertNotEqual(response.status_code, 200)

    def test_publications_page(self):
        response = self.client.get(reverse("publications"))
        self.assertNotEqual(response.status_code, 200)

    def test_publication_page(self):
        response = self.client.get(reverse("publication"))
        self.assertNotEqual(response.status_code, 200)

    def test_register_page(self):
        self.client.login(username="toto", password="123")
        response = self.client.get(reverse("register"))
        self.assertNotEqual(response.status_code, 200)

    def test_double_favourite(self):
        self.client.login(username="toto", password="123")
        self.client.get(reverse("add_to_favourites", args=[1]))
        self.client.get(reverse("add_to_favourites", args=[1]))
        self.assertTrue(UserFavouriteArticle.objects
                              .filter(user=self.user, article=self.article).count() == 1)

        


