from django.urls import path
from . import views

urlpatterns = [
    # Add the new address URL pattern
    path('add/<str:loginid>', views.AddAddressView.as_view()),
    path('<str:loginid>', views.GetAddressView.as_view()),
]
