from . import views
from django.urls import path

urlpatterns = [
    path("", views.GetAllUserView.as_view()),
    path("<int:id>", views.UserIDView.as_view()),
    path("register", views.AddUserView.as_view()),
    path("login", views.LoginUserView.as_view()),
    path("update/<int:id>", views.UpdateUserView.as_view()),
    path("delete/<int:id>", views.DeleteUserView.as_view()),
]
