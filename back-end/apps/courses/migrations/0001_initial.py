# Generated by Django 5.1.4 on 2024-12-11 16:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Course",
            fields=[
                (
                    "course_id",
                    models.UUIDField(
                        auto_created=True,
                        db_index=True,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("title", models.CharField(max_length=200)),
                ("description", models.TextField()),
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("published", models.BooleanField(default=False)),
                (
                    "instructor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="CourseContent",
            fields=[
                (
                    "content_id",
                    models.UUIDField(
                        auto_created=True,
                        db_index=True,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("title", models.CharField(max_length=200)),
                (
                    "content_type",
                    models.CharField(
                        choices=[
                            ("VIDEO", "Video"),
                            ("TEXT", "Text"),
                            ("QUIZ", "Quiz"),
                        ],
                        max_length=20,
                    ),
                ),
                ("video_url", models.URLField(blank=True, null=True)),
                ("content_text", models.TextField(blank=True, null=True)),
                ("order", models.IntegerField()),
                (
                    "course",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="contents",
                        to="courses.course",
                    ),
                ),
            ],
            options={
                "ordering": ["order"],
            },
        ),
        migrations.CreateModel(
            name="CourseEnrollment",
            fields=[
                (
                    "enrollment_id",
                    models.UUIDField(
                        auto_created=True,
                        db_index=True,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("enrolled_at", models.DateTimeField(auto_now_add=True)),
                ("completed", models.BooleanField(default=False)),
                ("progress", models.IntegerField(default=0)),
                (
                    "course",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="courses.course"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "unique_together": {("user", "course")},
            },
        ),
    ]
