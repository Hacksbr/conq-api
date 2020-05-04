from django.urls import reverse
from django.conf import settings
from django.http import HttpResponseRedirect

from rest_framework import viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response

from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from rest_auth.registration.views import SocialLoginView, SocialConnectView

from .models import User
from .serializers import UserSerializer


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]


def password_reset(request):
    return HttpResponseRedirect(reverse('account_reset_password'))


class CustomObtainAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({'token': token.key, 'id': token.user_id})


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter
    authentication_classes = [TokenAuthentication]


class FacebookConnect(SocialConnectView):
    adapter_class = FacebookOAuth2Adapter
    authentication_classes = [TokenAuthentication]


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = settings.GOOGLE_REDIRECT_URL
    client_class = OAuth2Client
    authentication_classes = [TokenAuthentication]
