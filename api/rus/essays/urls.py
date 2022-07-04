from django.urls import path

from .views import EssayCreate, EssayDetailView, EssayListView

urlpatterns = [
    path('pass/', EssayCreate.as_view(), name='essay_pass'),
    path('list_all/', EssayListView.as_view(), name='essays_list_all'),
    path('<slug:pk>/', EssayDetailView.as_view(), name='essay_detail'),
]
