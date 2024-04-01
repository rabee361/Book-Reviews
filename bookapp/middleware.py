from django.utils.deprecation import MiddlewareMixin
import logging

logger = logging.getLogger(__name__)

class CustomMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # This method is called before the view
        # You can modify the request here
        return None

    def process_response(self, request, response):
        # This method is called after the view
        # You can modify the response here
        request.test = "im testing bitch!!"
        return response
    




class CountRequestsMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
        self.count_requests = 0
        self.count_exceptions = 0

    def __call__(self, request, *args, **kwargs):
        self.count_requests += 1
        logger.info(f"Handled {self.count_requests} requests so far")
        print(self.count_requests)
        return self.get_response(request)

    def process_exception(self, request, exception):
        self.count_exceptions += 1
        logger.error(f"Encountered {self.count_exceptions} exceptions so far")







# class GZipMiddleware(CommonMiddleware):
#     """
#     Middleware class to enable Gzip compression for HTTP responses.
#     """
#     def __init__(self, get_response=None):
#         super().__init__(get_response)
#         self.get_response = get_response

#     @gzip_page
#     def __call__(self, request):
#         # Handle Gzip compression for HTTP responses
#         response = self.get_response(request)

#         # Set response headers to indicate Gzip compression
#         response['Content-Encoding'] = 'gzip'
#         response['Vary'] = 'Accept-Encoding'

#         return response