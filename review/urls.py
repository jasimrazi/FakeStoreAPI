from django.urls import path
from .views import AddReviewView

urlpatterns = [
    path('add/<int:product_id>/<str:loginid>', AddReviewView.as_view(), name='add_review'),
]
