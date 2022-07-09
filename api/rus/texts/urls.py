from django.urls import path

from .views import TextCreate, TextDetailView, TextListView, TextKeyCreateView

urlpatterns = [
    path('assign/', TextCreate.as_view(), name='text_assign'),
    path('list_all/', TextListView.as_view(), name='texts_list_all'),
    path('detail/<uuid:pk>/', TextDetailView.as_view(), name='text_detail'),
    path('keys/add/', TextKeyCreateView.as_view(), name='add_text_keys'),
]
