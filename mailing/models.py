from django.db import models
from guardian.shortcuts import assign_perm

from users.models import User

NULLABLE = {
    "blank": True,
    "null": True,
}


class Client(models.Model):
    email = models.EmailField()
    full_name = models.CharField(max_length=255)
    comment = models.TextField(**NULLABLE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        assign_perm("view_client", self.owner, self)
        assign_perm("change_client", self.owner, self)
        assign_perm("delete_client", self.owner, self)

    def __str__(self):
        return self.full_name


class Message(models.Model):
    subject = models.CharField(max_length=255)
    body = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.subject


class Mailing(models.Model):
    PERIODICITY_CHOICES = [
        ('daily', 'Раз в день'),
        ('weekly', 'Раз в неделю'),
        ('monthly', 'Раз в месяц'),
    ]
    STATUS_CHOICES = [
        ('created', 'Создана'),
        ('running', 'Запущена'),
        ('completed', 'Завершена'),
    ]

    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    periodicity = models.CharField(max_length=10, choices=PERIODICITY_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='created')
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    clients = models.ManyToManyField(Client, related_name='mailings')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Рассылка {self.id} - {self.get_status_display()}"


class MailingAttempt(models.Model):
    STATUS_CHOICES = [
        ('success', 'Успешно'),
        ('failed', 'Не успешно'),
    ]

    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, related_name='attempt')
    attempt_datetime = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    server_response = models.TextField(**NULLABLE)

    def __str__(self):
        return f"Попытка рассылки {self.mailing.id} - {self.get_status_display()}"
