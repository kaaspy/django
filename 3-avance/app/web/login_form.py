from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _

class fuck_this_web_crap(AuthenticationForm):
    def __init__(self, request = ..., *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.fields["username"].label = ""
        self.fields["password"].label = ""
        self.fields["username"].widget.attrs.update({
            'class': 'form-control form-control-sm',
            'placeholder': _("username"),
            'style': 'width: 200px;'
        })
        self.fields["password"].widget.attrs.update({
            'class': 'form-control form-control-sm',
            'placeholder': _("password"),
            'style': 'width: 200px;'
        })

def login_form(request):
    if not request.user.is_authenticated:
        return {"login_form": fuck_this_web_crap()}
    return {}