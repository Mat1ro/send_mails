from django.contrib import admin

from mailing.models import Client, Message, Mailing, Blog


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'email')
    search_fields = ('email',)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject')
    search_fields = ('subject', 'body')

@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('id', 'message')


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
