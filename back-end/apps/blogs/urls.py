from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_blogs, name='list-blogs'),
    path('create/', views.create_blog, name='create-blog'),
    path('<uuid:blog_id>/', views.get_blog, name='get-blog'),
    path('<uuid:blog_id>/update/', views.update_blog, name='update-blog'),
    path('<uuid:blog_id>/delete/', views.delete_blog, name='delete-blog'),
]
