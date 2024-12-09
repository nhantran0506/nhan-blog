from django.db import models


class Rating(models.Model):
    rating_id = models.UUIDField(primary_key = True, db_index = True, auto_created = True)
    rating_stars = models.IntegerField(default=0)
    user_comment = models.TextField(blank=True)
    