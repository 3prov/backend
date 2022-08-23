from django.urls import path
from .views import (
    StageAddView,
    SwitchStageAddView,
    StatisticsAddView,
    CurrentStageEndTime,
)

urlpatterns = [
    path('get_stage/', StageAddView.as_view(), name='get_stage'),
    path(
        'switch_stage_to_next/',
        SwitchStageAddView.as_view(),
        name='switch_stage_to_next',
    ),
    path('statistics/', StatisticsAddView.as_view(), name='statistics'),
    path(
        'get_current_stage_end_time/',
        CurrentStageEndTime.as_view(),
        name='get_current_stage_end_time',
    ),
]
