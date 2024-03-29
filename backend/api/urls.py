from django.urls import include, path

urlpatterns = [
    path('', include('api.foodgram.urls')),
    path('users/', include('api.users.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
