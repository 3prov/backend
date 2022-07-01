from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from . import views

urlpatterns = [
    path('docs/', include_docs_urls(title='3prov')),
    path('rus/', include('api.rus.urls')),
    path('users/', views.UserListView.as_view()),
    path('users/<slug:pk>', views.UserDetailView.as_view()),
]
