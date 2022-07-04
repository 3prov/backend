from django.urls import path

from .views import EssayCreate, EssayDetailView, EssayListView, EssayGetLinkToFormView

urlpatterns = [
    path('pass/', EssayCreate.as_view(), name='essay_pass'),
    path('list_all/', EssayListView.as_view(), name='essays_list_all'),
    path('<slug:pk>/', EssayDetailView.as_view(), name='essay_detail'),
    path('get_link_to_form', EssayGetLinkToFormView.as_view(), name='essay_get_link_to_form'),
]
