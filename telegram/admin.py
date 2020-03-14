from django.contrib import admin

# Register your models here.

from .models import PersonalUser, Message


@admin.register(PersonalUser)
class PersonalUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'telegram_id', 'is_staff')
    list_filter = ('is_staff', 'is_superuser')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'body', 'created', 'status')
    list_filter = ('status', )