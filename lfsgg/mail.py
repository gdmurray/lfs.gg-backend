import os
import json

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.parsers import BaseParser

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.http import HttpResponse

from lfsgg.utils import textify
from lfsgg.core.tokens import account_activation_token


class Mail:
    class Verify:
        from_email = "lfs.gg <no-reply@lfs.gg>"
        subject = "Verify your Email Address"

        @staticmethod
        def create_url(user):
            domain = settings.FRONTEND_URL
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = account_activation_token.make_token(user)
            url = f"{domain}/a/activate/{uid}/{token}"
            return url

        @staticmethod
        def send(to, from_email=from_email, subject=subject, variables={}):
            msg_html = render_to_string('email/core/verify_account.html', variables)
            msg_text = textify(msg_html)
            if type(to) != list:
                to = [to]

            send_mail(
                subject,
                msg_text,
                from_email,
                to,
                html_message=msg_html
            )

    class Beta:
        from_email = "beta@lfs.gg"
        # def send(self, ):

    class Password:
        from_email = "password@lfs.gg"

    class Billing:
        from_email = "billing@lfs.gg"


class PlainTextParser(BaseParser):
    """
    Plain text parser.
    """
    media_type = 'text/plain'

    def parse(self, stream, media_type=None, parser_context=None):
        """
        Simply return a string representing the body of the request.
        """
        return stream.read()


class AWSBounceHandler(APIView):
    permission_classes = (AllowAny,)
    parser_classes = (PlainTextParser,)

    def post(self, request, *args, **kwargs):
        data = json.loads(request.data.decode('utf-8'))
        print(data)
        return HttpResponse(status=200)


class AWSComplaintHandler(APIView):
    permission_classes = (AllowAny,)
    parser_classes = (PlainTextParser,)

    def post(self, request, *args, **kwargs):
        data = json.loads(request.data.decode('utf-8'))
        print(data)
        return HttpResponse(status=200)
