import json

from django.db import models
from django.utils import timezone

from jsonfield import JSONField

from sendgrid_events.signals import batch_processed


class Event(models.Model):
    kind = models.CharField(max_length=75)
    email = models.CharField(max_length=150)
    data = JSONField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    @classmethod
    def process_batch(cls, data):
        events = []
        for line in data.split("\r\n"):
            if line:
                d = json.loads(line.strip())
                events.append(Event.objects.create(
                    kind=d["event"],
                    email=d["email"],
                    data=d
                ))
        batch_processed.send(sender=Event, events=events)
        return events
