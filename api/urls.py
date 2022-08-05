from django.urls import path, include, re_path
from rest_framework.documentation import include_docs_urls
from . import views

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    re_path(
        r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0),
        name='schema-json',
    ),
    re_path(
        r'^swagger/$',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui',
    ),
    re_path(
        r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'
    ),
    path('docs/', include_docs_urls(title='3prov')),
    path('authtoken/', include('djoser.urls')),
    path('authtoken/', include('djoser.urls.authtoken'), name='djoser_url_token'),
    path('rus/', include('api.rus.urls')),
    path('users/', views.UserListView.as_view()),
    path('users/<uuid:pk>', views.UserDetailView.as_view()),
    path('management/', include('api.management.urls')),
    path('health_check/', views.health_check_view, name='health_check'),
]
