from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView

from users.forms import UserRegistrationForm, UserUpdateForm
from users.models import User


class RegisterView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = "register.html"
    success_url = reverse_lazy("index")


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'user_detail.html'

    def dispatch(self, request, *args, **kwargs):
        if self.get_object() != request.user:
            return HttpResponseForbidden("Вы не можете заходить на чужой профиль.")
        return super().dispatch(request, *args, **kwargs)


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'user_update_form.html'

    def dispatch(self, request, *args, **kwargs):
        if self.get_object() != request.user:
            return HttpResponseForbidden("Вы не можете редактировать чужой профиль.")
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('user-detail', kwargs={'pk': self.object.pk})
