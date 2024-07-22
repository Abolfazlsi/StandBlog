from django.contrib import admin
from django.urls import path, include
from standblog import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", include("home.urls")),
    path("", include("accounts.urls")),
    path("articles/", include("blog.urls")),
    path('admin/', admin.site.urls),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
