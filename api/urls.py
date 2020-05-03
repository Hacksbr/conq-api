from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from .views import redirect_view
from rest_framework import routers
from accounts.views import (
    UsersViewSet, CustomObtainAuthToken,
    FacebookLogin, FacebookConnect, GoogleLogin,
    password_reset
)

router = routers.DefaultRouter()
router.register(r'users', UsersViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('accounts/new-password/', password_reset),
    path('auth/facebook/', FacebookLogin.as_view(), name='fb_login'),
    path('auth/facebook/connect/', FacebookConnect.as_view(), name='fb_connect'),
    path('auth/google/', GoogleLogin.as_view(), name='google_login'),
    path('api/v1/', include(router.urls)),
    path('auth/', CustomObtainAuthToken.as_view()),
    path('api-auth/', include('rest_framework.urls')),

    path('', redirect_view),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
