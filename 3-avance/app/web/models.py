from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class Article(models.Model):
    title = models.CharField(
        max_length=64,
        null=False,
        verbose_name=_("Title"),
        )
    author = models.ForeignKey(
        User,
        db_column="user",
        on_delete=models.CASCADE,
        null=False,
        verbose_name=_("Author"),
    )
    created = models.DateTimeField(
        null=False,
        auto_now_add=True,
        verbose_name=_("Created"),
    )
    synopsis = models.CharField(
        max_length=312,
        null=False,
        verbose_name=_("Synopsis"),
        )
    content = models.TextField(
        null=False,
        verbose_name=_("Content"),
    )

    def __str__(self):
        return self.title

class UserFavouriteArticle(models.Model):
    user = models.ForeignKey(
        User,
        db_column="user",
        on_delete=models.CASCADE,
        null=False,
        verbose_name=_("User"),
    )
    article = models.ForeignKey(
        Article,
        db_column="article",
        on_delete=models.CASCADE,
        null=False,
        verbose_name=_("Article"),
    )

    def __str__(self):
        return self.article.title