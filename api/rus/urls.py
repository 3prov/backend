from django.urls import path, include

from api.rus.views import TextCreate

urlpatterns = [
    path('text_assign', TextCreate.as_view()),
]
