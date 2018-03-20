
from django_apistar.apps import App
from django.http.response import HttpResponseNotFound
from django.utils.deprecation import MiddlewareMixin


class RequestMiddleware(MiddlewareMixin):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.response_headers = []
        self.status_text = ''

    def process_apistar_response(self, status_text, headers):
        self.status_text = status_text
        self.response_headers = headers

    def process_response(self, request, response):
        path = request.environ['PATH_INFO']

        if path != '/' and not isinstance(response, HttpResponseNotFound):
            return response

        if not path.endswith('/') and not path.endswith('.js'):
            request.environ['PATH_INFO'] = path + '/'

        content = App(request.environ, self.process_apistar_response)

        if content:
            response.content = content
            response._headers['content-type'] = self.response_headers[0]
            response.status_code = int(self.status_text.split(' ')[0])

        return response
