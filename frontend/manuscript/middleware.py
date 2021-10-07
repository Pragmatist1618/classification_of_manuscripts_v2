class MyMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response['Pragma-directive'] = "no-cache"
        response['Cache-directive'] = "no-cache"
        response['Cache-control'] = "no-cache"
        response['Pragma'] = "no-cache"
        response['Expires'] = "0"

        return response

