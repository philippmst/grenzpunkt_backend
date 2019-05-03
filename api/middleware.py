from django.contrib.auth.models import User

class GetUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        # print("User.objects.first(): {}".format(User.objects.first()))
        # request.user = User.objects.first()

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response