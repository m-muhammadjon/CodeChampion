from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("social-auth/", include("social_django.urls", namespace="social")),
    path("", include("apps.base.urls", namespace="base")),
    path("", include("apps.users.urls", namespace="users")),
    path("", include("apps.problems.urls", namespace="problems")),
    path("", include("apps.contests.urls", namespace="contests")),
]
urlpatterns += [
    path("ckeditor/", include("ckeditor_uploader.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
