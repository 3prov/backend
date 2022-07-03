from django.urls import path, include

from api.rus.views import TextCreate, TextDetailView, TextListView

urlpatterns = [
    path('text_assign', TextCreate.as_view(), name='text_assign'),
    path('texts_list_all', TextListView.as_view(), name='texts_list_all'),
    path('text_detail/<slug:pk>', TextDetailView.as_view(), name='text_detail'),
]
