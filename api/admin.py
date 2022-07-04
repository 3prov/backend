from django.contrib import admin
from .models import User, FormURL
from .rus.models import Text, Essay, TextKey
from .management.models import Stage, WeekID


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username',)


@admin.register(Text)
class TextAdmin(admin.ModelAdmin):
    list_display = ('id',)


@admin.register(Essay)
class EssayAdmin(admin.ModelAdmin):
    list_display = ('id',)


@admin.register(Stage)
class StageAdmin(admin.ModelAdmin):
    list_display = ('stage', )


@admin.register(WeekID)
class WeekIDAdmin(admin.ModelAdmin):
    pass


@admin.register(TextKey)
class TextKeyAdmin(admin.ModelAdmin):
    list_display = ('id', )


@admin.register(FormURL)
class FormURLAdmin(admin.ModelAdmin):
    list_display = ('user', 'week_id', )
    readonly_fields = ('url', )

