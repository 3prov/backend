from django.urls import path

from .views import EssayDecodeURLView, EvaluationDecodeURLView
from ..rus.results.views import WeekResultsFromFormURLListView

urlpatterns = [
    path(
        'work/<str:encoded_part>/',
        EssayDecodeURLView.as_view(),
        name='form_essay_by_encoded_part',
    ),
    path(
        'evaluation/<str:encoded_part>/',
        EvaluationDecodeURLView.as_view(),
        name='form_evaluation_by_encoded_part',
    ),
    path(
        'results/<str:encoded_part>/',
        WeekResultsFromFormURLListView.as_view(),
        name='week_results_list_by_encoded_part',
    ),
]
