from django.urls import path

from .views import DecodeURLView

urlpatterns = [
    path('<slug:encoded_part>/', DecodeURLView.as_view(), name='form_distribution_by_encoded_part'),
]
