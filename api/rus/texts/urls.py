from django.urls import path

from .views import TextCreate, TextDetailView, TextListView

urlpatterns = [
    path('assign/', TextCreate.as_view(), name='text_assign'),
    path('list_all/', TextListView.as_view(), name='texts_list_all'),
    path('<slug:pk>/', TextDetailView.as_view(), name='text_detail'),
]
