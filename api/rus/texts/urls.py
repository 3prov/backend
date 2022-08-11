from django.urls import path

from .views import (
    TextCreate,
    TextView,
    TextListView,
    TextKeyCreateView,
    TextByFormURLView,
)

urlpatterns = [
    path('assign/', TextCreate.as_view(), name='text_assign'),
    path('list_all/', TextListView.as_view(), name='texts_list_all'),
    path('<uuid:pk>/', TextView.as_view(), name='text_detail'),
    path('keys/add/', TextKeyCreateView.as_view(), name='add_text_keys'),
    path(
        'get_by_results_form_url/<str:encoded_part>/',
        TextByFormURLView.as_view(),
        name='text_get_by_results_form_url',
    ),
]
