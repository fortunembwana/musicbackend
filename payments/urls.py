from django.urls import path
from .views import PaymentUploadView

urlpatterns = [
    path('upload/', PaymentUploadView.as_view(), name='payment-upload'),
]