from django.db import models
from django.contrib.auth.models import User


class Ad(models.Model):
    CATEGORY_CHOICES = [
        ('cars', 'Автомобили'),
        ('items', 'Личные вещи'),
        ('devices', 'Техника'),
        ('home', 'Для дома'),
        ('hobby', 'Хобби и отдых'),
        ('other', 'Другое'),
    ]

    CONDITION_CHOICES = [
        ('new', 'Новый'),
        ('used', 'Б/У'),
        ('bad', 'сильно Б/У')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ads')
    title = models.CharField(max_length=255)
    description = models.TextField()
    image_url = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=15, choices=CATEGORY_CHOICES)
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ExchangeOffer(models.Model):
    STATUS_CHOICES = [
        ('pending', 'ожидает'),
        ('accepted', 'принята'),
        ('declined', 'отклонена')
    ]

    ad_sender = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='sent_offers')
    ad_receiver = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='received_offers')
    comment = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ad_sender} → {self.ad_receiver} [{self.status}]"
