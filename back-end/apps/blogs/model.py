from django.db import models


class Blog(models.Model):
    blog_id = models.UUIDField(primary_key = True, db_index = True, auto_created = True)
    blog_content = models.TextField()