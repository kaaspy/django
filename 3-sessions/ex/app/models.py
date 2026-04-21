from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Tip(models.Model):
    content = models.TextField()
    author = models.ForeignKey(
        User,
        db_column="user",
        on_delete=models.CASCADE
    )
    date = models.DateTimeField(
        null=False,
        auto_now_add=True
    )
    @property
    def upvotes(self):
        return self.votes.filter(nature=Vote.Nature.UPVOTE).count()
    @property
    def downvotes(self):
        return self.votes.filter(nature=Vote.Nature.DOWNVOTE).count()

class Vote(models.Model):
    class Nature(models.IntegerChoices):
        UPVOTE = 1, "Up"
        DOWNVOTE = 2, "Down"
    nature = models.IntegerField(
        choices=Nature.choices,
    )
    author = models.ForeignKey(
        User,
        db_column="user",
        on_delete=models.CASCADE,
        related_name="votes",
    )
    tip = models.ForeignKey(
        Tip,
        db_column="tip",
        on_delete=models.CASCADE,
        related_name="votes",
    )
    class Meta:
        unique_together = ("tip", "author")
