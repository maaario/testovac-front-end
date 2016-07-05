from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class ExtendedUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(ExtendedUserCreationForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].required = True

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
