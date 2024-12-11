from django.db import models
from apps.users.model import User

class Blog(models.Model):
    blog_id = models.UUIDField(primary_key=True, db_index=True, auto_created=True)
    title = models.CharField(max_length=200)
    blog_content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title 