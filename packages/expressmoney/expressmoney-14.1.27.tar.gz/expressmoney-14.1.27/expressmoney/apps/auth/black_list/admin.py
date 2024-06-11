from django.contrib import admin

from .models import BlackList


@admin.register(BlackList)
class BlackListAdmin(admin.ModelAdmin):
    list_display = ('created', 'user_id', 'passport_serial', 'passport_number', 'cause', 'comment')
    search_fields = ('=user_id', '=passport_number')
    list_filter = ('cause',)
    ordering = ('-created', )
