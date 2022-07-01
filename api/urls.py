from django.urls import path, include
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    path('docs/', include_docs_urls(title='3prov')),
    path('rus/', include('api.rus.urls')),
]
