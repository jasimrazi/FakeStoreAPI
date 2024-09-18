from cart import views
from django.urls import path

urlpatterns = [
    path("", views.GetAllCartItemsView.as_view()),
    path("add/<int:userid>", views.AddToCartView.as_view()),
    path("user/<int:userid>", views.GetCartItemUserID.as_view()),
    path("update/<int:userid>", views.UpdateCartView.as_view()),
    
]
