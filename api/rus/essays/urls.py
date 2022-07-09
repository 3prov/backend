from django.urls import path

from .views import EssayCreate, EssayDetailView, EssayListView, EssayFormURLUserCreate, EssayFromFormURLCreate, \
    EssayFormURLUserListView, EssayFromFormURLDetailView

urlpatterns = [
    path('pass/', EssayCreate.as_view(), name='essay_pass'),  # ?
    path('list_all/', EssayListView.as_view(), name='essays_list_all'),
    path('detail/<uuid:pk>/', EssayDetailView.as_view(), name='essay_detail'),  # ?
    path('create_link_to_form/', EssayFormURLUserCreate.as_view(), name='create_link_to_essay_form'),
    path('get_user_form_links/<uuid:user>/', EssayFormURLUserListView.as_view(), name='get_user_essay_form_links'),
    path('form-url/<str:encoded_part>/post/', EssayFromFormURLCreate.as_view(), name='essay_from_url_post'),  # Create
    path('form-url/<str:encoded_part>/edit/', EssayFromFormURLDetailView.as_view(), name='essay_from_url_edit'),  # Read, Update
]
