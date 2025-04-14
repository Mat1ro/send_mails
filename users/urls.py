from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.views import RegisterView, UserDetailView, UserUpdateView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(template_name="login.html"), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user/<int:pk>', UserDetailView.as_view(), name='user-detail'),
    path('user/<int:pk>/edit', UserUpdateView.as_view(), name='user-update'),
]
