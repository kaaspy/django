from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    def __init__(self, request = ..., *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.fields["username"].label = ""
        self.fields["password"].label = ""
        self.fields["username"].widget.attrs.update({
            'class': 'form-control',
            'placeholder': "username",
            'style': 'width: 200px;'
        })
        self.fields["password"].widget.attrs.update({
            'class': 'form-control',
            'placeholder': "password",
            'style': 'width: 200px;'
        })

def login_form(request):
    return {"login_form": LoginForm()}
