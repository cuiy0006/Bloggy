from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.forms import PasswordChangeForm
from users.models import User

class RegisterFrom(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "nickname", "first_name", "last_name", "email")

# class PwdChangeForm(PasswordChangeForm):
#     class Meta(PasswordChangeForm.Meta):
#         model = User