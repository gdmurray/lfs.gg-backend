from django.utils.deprecation import MiddlewareMixin


class AccessLogMiddleware(MiddlewareMixin):
    def process_request(self, request):
        return

    def process_response(self, request, response):
        return response
