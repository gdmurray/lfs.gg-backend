from django.shortcuts import render
from django.http import HttpResponse

from .serializers import *
from .forms import SignupForm
from .tokens import account_activation_token

from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.parsers import BaseParser
from rest_framework import status
from lfsgg.mail import Mail

from rest_framework_simplejwt.tokens import RefreshToken


class RegisterView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        form = SignupForm(request.data)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.save()

            refresh = RefreshToken.for_user(user)
            url = Mail.Verify.create_url(user)
            Mail.Verify.send(to=[user.email], variables={'cta_url': url})
            return Response(data={
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }, status=200)
        else:
            print(form.errors)
            return Response(data=form.error_messages, status=500)


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.email_confirmed = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you are verified')
    else:
        return HttpResponse('Activation link is invalid!')


class EchoView(APIView):
    def post(self, request, *args, **kwarg):
        serializer = EchoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED
        )


class UserDataView(APIView):
    def get(self, request, *args, **kwargs):
        serializer = UserDataSerializer(request.user, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)


def test_template(request):
    return render(request, 'email/password/reset_password.html')


def test_email_send(request):
    to = ['gd-murray@hotmail.com']
    Mail.Verify.send(to=to)
    return HttpResponse(f"Sent to {to}")
