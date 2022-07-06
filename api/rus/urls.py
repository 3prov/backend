from django.urls import path, include


urlpatterns = [
    path('text/', include('api.rus.texts.urls')),
    path('essay/', include('api.rus.essays.urls')),
    path('evaluation/', include('api.rus.evaluations.urls')),
]
