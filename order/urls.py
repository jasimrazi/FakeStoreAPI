# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('create/<str:loginid>', views.OrderCreateView.as_view(), name='create_order'),
    path('<str:loginid>', views.UserOrderListView.as_view(), name='user_orders'),
]
