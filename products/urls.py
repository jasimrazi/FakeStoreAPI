from . import views
from django.urls import path

urlpatterns = [
    path("", views.GetProductsView.as_view()),
    path("add", views.AddProductView.as_view()),
    path('<int:productid>/', views.ProductIDView.as_view()),
    path("categories", views.AllCategoriesView.as_view()),
    path("categories/<str:category>", views.SpecificCategoryView.as_view()),
    path("update/<int:id>", views.UpdateProductView.as_view()),
    path("delete/<int:id>", views.DeleteProductView.as_view()),
]
