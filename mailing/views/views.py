from django.shortcuts import render

from mailing.models import Client, Message, Mailing, Blog


def index(request):
    context = {
        'total_clients': Client.objects.count(),
        'total_messages': Message.objects.count(),
        'total_mailings': Mailing.objects.count(),
        'active_mailings': Mailing.objects.filter(status='active').count(),
        'latest_blogs': Blog.objects.order_by('-created')[:3],
    }
    for i in  Blog.objects.order_by('-created')[:3]:
        i.views += 1
        i.save()
    return render(request, 'index.html', context)


