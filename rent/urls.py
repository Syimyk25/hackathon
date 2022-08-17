from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
    openapi.Info(
        title='Hackaton',
        default_version='v1',
        description='Created by \nDzhumabaev Syimyk'
    ),
    public=True
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/account/', include('applications.account.urls')),
    path('api/v1/cars/', include('applications.cars.urls')),
    path('api/v1/notifications/', include('applications.notifications.urls')),
    path('swagger/', schema_view.with_ui('swagger')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

