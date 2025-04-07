from datetime import datetime, timezone

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.mail import send_mail

from mailing.models import Mailing, MailingAttempt
from send_mails import settings


def send(mailing: Mailing):
    try:
        message = mailing.message
        clients = mailing.clients.all()
        emails = []
        for client in clients:
            emails.append(client.email)
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
        attempt_datetime=datetime.now(timezone.utc),
        status=status,
        server_response=response_text
    )


def check_mailings():
    from mailing.models import Mailing
    current_time = datetime.now(timezone.utc)
    running_mailings = []

    for mailing in Mailing.objects.all():
        if mailing.end_datetime > current_time > mailing.start_datetime:
            mailing.status = 'running'
            mailing.save()
        if mailing.status != 'running':
            continue
        if current_time > mailing.end_datetime:
            mailing.status = 'completed'
            mailing.save()
            continue


        running_mailings.append(mailing)

    for mailing in running_mailings:
        if mailing.periodicity == 'daily':
            send(mailing)
        elif mailing.periodicity == 'weekly':
            if current_time.weekday() == 0:
                send(mailing)
        elif mailing.periodicity == 'monthly':
            if current_time.day == 1:
                send(mailing)


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_mailings, trigger=CronTrigger(hour=9, minute=0))
    scheduler.start()
