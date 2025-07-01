import json
import os
from django.conf import settings
from django.shortcuts import redirect

USER_JSON_PATH = os.path.join(settings.BASE_DIR, 'meine_app', 'backend', 'registrierung_login', 'users.json')

def check_login(view_func):
    def wrapper(request, *args, **kwargs):
       
        return redirect("/login")

    return wrapper
