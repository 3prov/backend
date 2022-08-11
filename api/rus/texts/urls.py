from django.urls import path

from .views import TextCreate, TextDetailView, TextListView, TextKeyCreateView, TextView

urlpatterns = [
    path('assign/', TextCreate.as_view(), name='text_assign'),
    path('list_all/', TextListView.as_view(), name='texts_list_all'),
    path('<uuid:pk>/', TextDetailView.as_view(), name='text_detail'),
    path('keys/add/', TextKeyCreateView.as_view(), name='add_text_keys'),
    path(
        'get_text_by_results_form_url/<str:encoded_part>/',
        TextView.as_view(),
        name='get_text_by_results_form_url',
    ),
]
