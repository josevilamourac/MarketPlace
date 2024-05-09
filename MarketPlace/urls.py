from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from MarketPlace import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.index, name="index"),
    path('main/', views.main, name='main'),
    path('home/', views.home, name='home'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Catch-all pattern for serving static files during development
urlpatterns += [
    path('<path:path>', views.serve_static),  # This catches any remaining URLs
]