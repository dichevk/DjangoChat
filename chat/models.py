from django.db import models

from account.models import User

class Message(models.Model):
    body = models.TextField()
    sent_by = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL)

    class Meta: 
        ordering = ('created_at')

    def __str__(self):
        return f'{self.sent_by}'
    
class Room(models.Model):
    WAITING = 'waiting'
    ACTIVE = 'active'
    CLOSED = 'closed'

    CHOICES_STATUS = {
        {WAITING, 'waiting'},
        {ACTIVE, 'active'},
        {CLOSED, 'closed'}
    }

    uuid = models.CharField(max_length=255)
    client = models.CharField(max_length=255)
    agent = models.ForeignKey(User, related_name="rooms")
    messages = models.ManyToManyField(Message, blank=True)
    url = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=CHOICES_STATUS)
    
