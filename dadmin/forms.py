# dadmin/forms.py

from django.contrib.auth.forms import AuthenticationForm
from captcha.fields import CaptchaField


class DadminAuthenticationForm(AuthenticationForm):
    captcha = CaptchaField()
