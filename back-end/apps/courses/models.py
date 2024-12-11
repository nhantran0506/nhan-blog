from django.db import models
from apps.users.model import User

class Course(models.Model):
    course_id = models.UUIDField(primary_key=True, db_index=True, auto_created=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    instructor = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class CourseContent(models.Model):
    content_id = models.UUIDField(primary_key=True, db_index=True, auto_created=True)
    course = models.ForeignKey(Course, related_name='contents', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content_type = models.CharField(max_length=20, choices=[
        ('VIDEO', 'Video'),
        ('TEXT', 'Text'),
        ('QUIZ', 'Quiz')
    ])
    video_url = models.URLField(null=True, blank=True)
    content_text = models.TextField(null=True, blank=True)
    order = models.IntegerField()

    class Meta:
        ordering = ['order']

class CourseEnrollment(models.Model):
    enrollment_id = models.UUIDField(primary_key=True, db_index=True, auto_created=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    progress = models.IntegerField(default=0)  # Percentage of completion

    class Meta:
        unique_together = ['user', 'course'] 