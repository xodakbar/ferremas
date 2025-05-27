from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_payment, name='create_payment'),
    path('response/', views.webpay_response, name='webpay_response'),
    path('error/', views.payment_error, name='payment_error'),
]