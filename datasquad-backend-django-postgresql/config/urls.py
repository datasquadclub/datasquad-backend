from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve as static_serve

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("tracking.urls")),
    path("api/", include("content.urls")),
    # Sert les photos uploadées depuis l'admin (actus, équipe). Volume
    # persistant recommandé sur Railway -- voir README.
    re_path(r"^media/(?P<path>.*)$", static_serve, {"document_root": settings.MEDIA_ROOT}),
]
