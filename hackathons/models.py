from django.db import models
from users.models import User
import uuid

class Hackathon(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    title = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    background_image = models.URLField(null=True, blank=True)
    hackathon_image = models.URLField(null=True, blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    reward_prize = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = "hackathons"
        verbose_name = "hackathon"
        verbose_name_plural = "hackathons"

    def __str__(self):
        return "Hackathon - {title}".format(
            title=self.title,
        )
        
class HackathonRegister(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    hackathon = models.ForeignKey(Hackathon, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "hackathon_registers"
        verbose_name = "Hackathon Register"
        verbose_name_plural = "Hackathon Registers"

    def __str__(self):
        return "{user} - {hackathon}".format(
            user=self.user,
            hackathon=self.hackathon,
        )