from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from posts.api_views import PostListCreateAPIView, PostRetrieveUpdateDestroyAPIView

from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('posts.urls')),
    path('users/', include('users.urls')),
    path('Quillshelf/', include('Quillshelf.urls')),
    path('api/drf/posts/', PostListCreateAPIView.as_view(), name='drf-post-list'),
    path('api/drf/posts/<int:pk>/', PostRetrieveUpdateDestroyAPIView.as_view(), name='drf-post-detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

#hello world