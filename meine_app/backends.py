import json
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
import os
from django.conf import settings


USER_JSON_PATH = os.path.join(
    settings.BASE_DIR,
    'meine_app',
    'backend',
    'registrierung_login',
    'users.json'
)

class JSONAuthBackend:
    def authenticate(self, request, username=None, password=None):
        try:
            with open(USER_JSON_PATH, 'r') as f:
                users = json.load(f)

            for user_data in users:
                if user_data['username'] == username:
                     


                    # Check if the password matches
                    if check_password(password, user_data['password']):
                        try:
                            user = User.objects.get(username=username)
                        except User.DoesNotExist:
                            # Create a Django user object but don't save to database
                            user = User(
                                username=username,
                                email=user_data['email'],
                            )
                            user.set_unusable_password()
                            user.save()
                        return user
        except Exception as e:
            print(f"Error during authentication: {e}")
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None