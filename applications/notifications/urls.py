from rest_framework.routers import DefaultRouter

from applications.notifications.views import ContactSuvView

router = DefaultRouter()
router.register('suv', ContactSuvView)

urlpatterns = []
urlpatterns.extend(router.urls)