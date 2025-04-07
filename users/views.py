from django.urls import reverse_lazy
from django.views.generic import CreateView

from users.forms import UserRegistrationForm
from users.models import User


class RegisterView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = "register.html"
    success_url = reverse_lazy("index")