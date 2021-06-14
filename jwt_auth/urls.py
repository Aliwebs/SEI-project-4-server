from django.urls import path
from .views import LoginView, RegisterView, ProfileView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('profile/<str:pk>/', ProfileView.as_view())
]
