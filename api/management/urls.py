from django.urls import path
from .views import StageAddView, SwitchStageAddView

urlpatterns = [
    path('get_stage', StageAddView.as_view(), name='get_stage'),
    path('switch_stage_to_next', SwitchStageAddView.as_view(), name='switch_stage_to_next'),
]
