from favourite import views
from django.urls import path

urlpatterns = [
    path("add/<int:userid>", views.AddToFavouritesView.as_view()),  # Add an item to favourites
    path("user/<int:userid>", views.GetFavouritesByUserIDView.as_view()),  # Get all favourite items of a specific user
    path("delete/<int:userid>/<int:product_id>", views.DeleteFavouriteView.as_view()),  # Delete a favourite item
]
