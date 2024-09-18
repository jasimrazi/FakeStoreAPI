from cart import views
from django.urls import path

urlpatterns = [
    path("add/<int:userid>", views.AddToCartView.as_view()),
    
]
