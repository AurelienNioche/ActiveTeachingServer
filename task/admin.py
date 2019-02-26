from django.contrib import admin

# Register your models here.
from . models import User, Data


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id", "username", "gender", "age", "mother_tongue", "other_language", "registration_time")


class DataAdmin(admin.ModelAdmin):
    list_display = (
        "id", "user_id", "t", "question", "reply")


admin.site.register(User, UserAdmin)
admin.site.register(Data, DataAdmin)
