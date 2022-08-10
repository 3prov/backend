from django.urls import path

from api.rus.results.views import (
    WeekResultsListView,
    WeekResultsFormURLUserListView,
    RateEssayEvaluationFromFormURLCreate,
)

urlpatterns = [
    path('', WeekResultsListView.as_view(), name='week_results_list'),
    path(
        'get_link_to_form/<uuid:user>/',
        WeekResultsFormURLUserListView.as_view(),
        name='create_link_to_week_results_form',
    ),
    path(
        'rate_essay_evaluation/<str:encoded_part>/post/',
        RateEssayEvaluationFromFormURLCreate.as_view(),
        name='rate_essay_evaluation',
    ),
]
