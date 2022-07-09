from django.urls import path

from api.rus.evaluations.views import EvaluationFormURLGetCurrentWeekList, EssaySentenceReviewCreate, \
    EvaluationFormURLListView, EvaluationFormURLCreate, EvaluationFormURLView

urlpatterns = [
    #path('get_user_link_to_form/<uuid:user>/', name='get_user_list_to_evaluate_form'),
    path(
        'get_current_week_distribution/',
        EvaluationFormURLGetCurrentWeekList.as_view(),
        name='get_current_week_distribution'
    ),
    path('sentence_review/', EssaySentenceReviewCreate.as_view(), name='evaluation_essay_sentence_review'),
    path(
        'get_form_urls/<uuid:user>',
        EvaluationFormURLListView.as_view(),
        name='participant_get_urls_to_evaluate'
    ),
    path(
        'form-url/<str:encoded_part>/post/',
        EvaluationFormURLCreate.as_view(),
        name='evaluation_from_url_post'
    ),  # Create
    path(
        'form-url/<str:encoded_part>/edit/',
        EvaluationFormURLView.as_view(),
        name='evaluation_form_url_edit'
    ),  # Read, Update


]
