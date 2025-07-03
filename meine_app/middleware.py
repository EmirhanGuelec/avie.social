from django.http import HttpResponseForbidden

WHITELIST = {'[2a02:3100:6124:7300:60f8:cc61:66e7:c244]
'}

class IPWhitelistMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = request.META.get('REMOTE_ADDR')
        if ip not in WHITELIST:
            return HttpResponseForbidden("Zugriff nur von erlaubten IPs")
        return self.get_response(request)
