from django.db import models

# Create your models here.
import uuid
class ChatUuid(models.Model):
    chatuuid = models.UUIDField(unique=True, default=uuid.uuid4,
                                editable=False, help_text="The UUID for a Chatbot conversation.")
    created = models.DateTimeField(auto_now_add=True)
    agreed = models.TextField(
        blank=True, help_text="If user agreed to the service terms (http://...), send 'Einverstanden'.")

    def __str__(self):
        return str(self.chatuuid)


class ChatDialogue(models.Model):
    chatuuid = models.UUIDField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    input = models.TextField(blank=False)
    probability = models.FloatField(blank=True)
    understood = models.BooleanField(blank=True)
    output = models.TextField(blank=True)

    def __str__(self):
        return str(self.input)
