from django.urls import path

from api.rus.results.views import WeekResultsListView, WeekResultsFormURLUserCreate

urlpatterns = [
    path('', WeekResultsListView.as_view(), name='week_results_list'),
    path(
        'create_link_to_form/',
        WeekResultsFormURLUserCreate.as_view(),
        name='create_link_to_week_results_form',
    ),
]
