from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from guardian.mixins import PermissionRequiredMixin

from mailing.forms import MailingForm
from mailing.models import Mailing


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = 'mailing_list.html'

    def get_queryset(self):
        return Mailing.objects.filter(owner=self.request.user)


class MailingDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Mailing
    template_name = 'mailing_detail.html'
    permission_required = 'mailing.view_mailing'
    raise_exception = True


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing_form.html'
    success_url = reverse_lazy('mailing_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.cleaned_data['status'] = 'created'
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing_form.html'
    success_url = reverse_lazy('mailing_list')
    permission_required = 'mailing.change_mailing'
    raise_exception = True


class MailingDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Mailing
    template_name = 'mailing_confirm_delete.html'
    success_url = reverse_lazy('mailing_list')
    permission_required = 'mailing.delete_mailing'
    raise_exception = True


@method_decorator(require_POST, name='dispatch')
class MailingStartView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Mailing
    permission_required = 'mailing.change_mailing'
    raise_exception = True

    def post(self, request, *args, **kwargs):
        mailing = self.get_object()
        if mailing.status == 'created':
            mailing.status = 'running'
            mailing.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False}, status=400)
