from django.urls import path, include

from api.rus.views import TestAddView

urlpatterns = [
    path('hello', TestAddView.as_view()),
]
