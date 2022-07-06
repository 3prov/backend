from django.contrib import admin
from .models import User, FormURL
from .rus.evaluations.models import EssayEvaluation, EssayCriteria
from .rus.models import Text, Essay, TextKey
from .management.models import Stage, WeekID
from .work_distribution.models import WorkDistributionToEvaluate


# TODO: move admins to their apps

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username']


@admin.register(Text)
class TextAdmin(admin.ModelAdmin):
    list_display = ['id']


@admin.register(Essay)
class EssayAdmin(admin.ModelAdmin):
    list_display = ['id']


@admin.register(Stage)
class StageAdmin(admin.ModelAdmin):
    list_display = ['stage']


@admin.register(WeekID)
class WeekIDAdmin(admin.ModelAdmin):
    pass


@admin.register(TextKey)
class TextKeyAdmin(admin.ModelAdmin):
    list_display = ['id']


@admin.register(FormURL)
class FormURLAdmin(admin.ModelAdmin):
    list_display = ['user', 'week_id']
    readonly_fields = ['url']


class EssayEvaluationInline(admin.StackedInline):
    model = EssayEvaluation
    min_num = 2


@admin.register(EssayCriteria)
class EssayCriteriaAdmin(admin.ModelAdmin):
    list_display = ['id']
    inlines = [EssayEvaluationInline]


@admin.register(WorkDistributionToEvaluate)
class WorkDistributionToEvaluateAdmin(admin.ModelAdmin):
    list_display = ['id']
