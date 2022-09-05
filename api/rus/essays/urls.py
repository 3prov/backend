from django.urls import path

from .views import (
    EssayListView,
    EssayFromFormURLCreate,
    EssayFromFormURLDetailView,
    EssayWithEvaluationsTextKeysView,
    EssayFormURLUserGetOrCreate,
)

urlpatterns = [
    path('list_all/', EssayListView.as_view(), name='essays_list_all'),
    path('<uuid:pk>/', EssayWithEvaluationsTextKeysView.as_view(), name='essay_detail'),
    path(
        'get_or_create_form_link/',
        EssayFormURLUserGetOrCreate.as_view(),
        name='get_or_create_essay_form_link',
    ),
    path(
        'form-url/<str:encoded_part>/post/',
        EssayFromFormURLCreate.as_view(),
        name='essay_from_url_post',
    ),  # Create
    path(
        'form-url/<str:encoded_part>/edit/',
        EssayFromFormURLDetailView.as_view(),
        name='essay_from_url_edit',
    ),  # Read, Update
]
