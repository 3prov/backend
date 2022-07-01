from django.contrib import admin
from api.models import User, AuthSocialID
from api.rus.models import Text, Essay


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username',)


@admin.register(Text)
class TextAdmin(admin.ModelAdmin):
    list_display = ('id',)


@admin.register(Essay)
class EssayAdmin(admin.ModelAdmin):
    list_display = ('id',)


@admin.register(AuthSocialID)
class EssayAdmin(admin.ModelAdmin):
    pass

