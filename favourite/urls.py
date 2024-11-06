from favourite import views
from django.urls import path

urlpatterns = [
    path("add/<str:loginid>", views.AddToFavouritesView.as_view()),  # Add an item to favourites
    path("user/<str:loginid>", views.GetFavouritesByLoginIDView.as_view()),  # Get all favourite items of a specific user
    path("delete/<str:loginid>/<int:product_id>", views.DeleteFavouriteView.as_view()),  # Delete a favourite item
]
