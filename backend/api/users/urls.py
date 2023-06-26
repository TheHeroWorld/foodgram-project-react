from django.urls import include, path
from rest_framework.routers import DefaultRouter
from djoser.urls import authtoken


from .views import CustomUserViewSet, SubscribeViewSet


urlpatterns = authtoken.urlpatterns

router = DefaultRouter()
router.register('subscriptions', SubscribeViewSet)
router.register('', CustomUserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls'))
]
