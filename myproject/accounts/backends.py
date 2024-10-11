from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=email)
            print(f'User found: {user.username}, Type: {user.user_type}')  # Debugging line
        except UserModel.DoesNotExist:
            print('User not found')  # Debugging line
            return None
        
        if user.check_password(password):
            return user
        print('Password mismatch')  # Debugging line
        return None
