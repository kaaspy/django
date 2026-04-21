from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        if perm == "app.can_downvote":
            return self.reputation >= 15
        if perm == "app.delete_tip":
            return self.reputation >= 30
        return super().has_perm(perm, obj)

    @property
    def reputation(self):
        from app.models import Vote #fix circular import
        votes = Vote.objects.filter(tip__author=self)
        rep = 0
        for v in votes:
            if v.nature == 1:
                rep += 5
            if v.nature == 2:
                rep -= 2
        return rep

    class Meta:
        permissions = [
            ("can_downvote", "Can downvote a tip"),
        ]