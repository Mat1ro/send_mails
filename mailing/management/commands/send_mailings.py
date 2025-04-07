from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from mailing.models import Mailing, MailingAttempt
from datetime import datetime, timezone

class Command(BaseCommand):
    help = 'Отправка активных рассылок клиентам'

    def handle(self, *args, **kwargs):
        now = datetime.now(timezone.utc)


        active_mailings = Mailing.objects.filter(
            start_datetime__lte=now,
            end_datetime__gte=now,
            status='running'
        )

        for mailing in active_mailings:
            message = mailing.message
            clients = mailing.clients.all()

            emails = []
            for client in clients:
                emails.append(client.email)

            try:
                send_mail(
                    subject=message.subject,
                    message=message.body,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=emails,
                )
                response_text = f"Emails sent successfully to {len(emails)} recipients."
                status = 'success'

            except Exception as e:
                response_text = f"Error: {str(e)}"
                status = 'failed'

            MailingAttempt.objects.create(
                mailing=mailing,
                attempt_datetime=now,
                status=status,
                server_response=response_text
            )



