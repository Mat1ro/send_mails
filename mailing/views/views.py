from django.shortcuts import render

from mailing.models import Client, Message, Mailing


def index(request):
    context = {
        'total_clients': Client.objects.count(),
        'total_messages': Message.objects.count(),
        'total_mailings': Mailing.objects.count(),
        'active_mailings': Mailing.objects.filter(status='active').count(),
    }
    return render(request, 'index.html', context)
