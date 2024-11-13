from cart import views
from django.urls import path

urlpatterns = [
    path("", views.GetAllCartItemsView.as_view()),
    path("add/<str:loginid>/<int:productid>/<str:size>", views.AddToCartView.as_view()),
    path("user/<str:loginid>", views.GetCartItemUserID.as_view()),
    path("update/<str:loginid>", views.UpdateCartView.as_view()),
    path("delete/<str:loginid>", views.DeleteCartView.as_view()),
]
