from django.urls import path
from .views import AddReviewView, GetReviewView

urlpatterns = [
    path('add/<int:product_id>/<str:loginid>', AddReviewView.as_view()),
    path('<int:product_id>', GetReviewView.as_view()),
]
