
from django.urls import path

from account.views import RegisterView, LoginView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login-user/', LoginView.as_view())
]
