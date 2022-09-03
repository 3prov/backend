from django.urls import path

from api.rus.evaluations.views import (
    EvaluationFormURLGetCurrentWeekList,
    EssaySelectionReviewFromFormURLCreate,
    EvaluationFormURLListView,
    EvaluationFormURLWorkCreate,
    EvaluationFormURLView,
    WorkDistributionToEvaluateVolunteerListView,
    EssaySelectionReviewFormURLView,
    EvaluationFormURLVolunteerCreate,
)

urlpatterns = [
    path(
        'get_current_week_distribution/',
        EvaluationFormURLGetCurrentWeekList.as_view(),
        name='get_current_week_distribution',
    ),
    path(
        'selection_review/form-url/<str:encoded_part>/post/',
        EssaySelectionReviewFromFormURLCreate.as_view(),
        name='evaluation_essay_selection_review_form_url_post',
    ),  # Create
    path(
        'selection_review/form-url/<str:encoded_part>/edit/<int:start_selection_char_index>/<int:selection_length>/',
        EssaySelectionReviewFormURLView.as_view(),
        name='evaluation_essay_selection_review_form_url_edit',
    ),  # Read, Update
    path(
        'get_form_urls/<uuid:user>/',
        EvaluationFormURLListView.as_view(),
        name='participant_get_urls_to_evaluate',
    ),
    path(
        'form-url/<str:encoded_part>/post/',
        EvaluationFormURLWorkCreate.as_view(),
        name='evaluation_from_url_post',
    ),  # Create
    path(
        'form-url/<str:encoded_part>/edit/',
        EvaluationFormURLView.as_view(),
        name='evaluation_from_url_edit',
    ),  # Read, Update
    path(
        'volunteer_get_distribution/<uuid:user>/',
        WorkDistributionToEvaluateVolunteerListView.as_view(),
        name='volunteer_get_distribution',
    ),
    path(
        'volunteer_create_next_and_get_form_urls/<uuid:user>/',
        EvaluationFormURLVolunteerCreate.as_view(),
        name='volunteer_create_next_and_get_form_urls_user',
    ),
]
