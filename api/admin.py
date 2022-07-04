from django.contrib import admin
from .models import User
from .rus.models import Text, Essay, TextKey
from .management.models import Stage


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


@admin.register(TextKey)
class TextKeyAdmin(admin.ModelAdmin):
    list_display = ('id', )
