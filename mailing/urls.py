from django.urls import path
from django.views.decorators.cache import cache_page

from mailing.views.blog_views import BlogCreateView
from mailing.views.client_views import ClientListView, ClientDetailView, ClientCreateView, ClientUpdateView, \
    ClientDeleteView
from mailing.views.maililng_views import MailingListView, MailingDetailView, MailingCreateView, MailingUpdateView, \
    MailingDeleteView, MailingStartView
from mailing.views.message_views import MessageListView, MessageDetailView, MessageCreateView, MessageUpdateView, \
    MessageDeleteView
from mailing.views.views import index

urlpatterns = [
    path('', cache_page(60)(index), name='index'),

    path('clients/', ClientListView.as_view(), name='client_list'),
    path('clients/<int:pk>/', ClientDetailView.as_view(), name='client_detail'),
    path('clients/create/', ClientCreateView.as_view(), name='client_create'),
    path('clients/<int:pk>/edit/', ClientUpdateView.as_view(), name='client_edit'),
    path('clients/<int:pk>/delete/', ClientDeleteView.as_view(), name='client_delete'),

    path('messages/', MessageListView.as_view(), name='message_list'),
    path('messages/<int:pk>/', MessageDetailView.as_view(), name='message_detail'),
    path('messages/create/', MessageCreateView.as_view(), name='message_create'),
    path('messages/<int:pk>/edit/', MessageUpdateView.as_view(), name='message_edit'),
    path('messages/<int:pk>/delete/', MessageDeleteView.as_view(), name='message_delete'),

    path('mailings/', MailingListView.as_view(), name='mailing_list'),
    path('mailings/<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
    path('mailings/create/', MailingCreateView.as_view(), name='mailing_create'),
    path('mailings/<int:pk>/edit/', MailingUpdateView.as_view(), name='mailing_edit'),
    path('mailings/<int:pk>/delete/', MailingDeleteView.as_view(), name='mailing_delete'),
    path('mailings/<int:pk>/start/', MailingStartView.as_view(), name='mailing_start'),

    path('blog/create/', BlogCreateView.as_view(), name='blog_create'),
]
