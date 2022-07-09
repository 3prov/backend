from django.urls import path

from .views import EssayDecodeURLView, EvaluationDecodeURLView

urlpatterns = [
    path('w/<str:encoded_part>/', EssayDecodeURLView.as_view(), name='form_essay_by_encoded_part'),
    path('e/<str:encoded_part>/', EvaluationDecodeURLView.as_view(), name='form_evaluation_by_encoded_part'),
]
