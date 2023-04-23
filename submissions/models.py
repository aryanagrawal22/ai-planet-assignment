from django.db import models
from hackathons.models import Hackathon
from users.models import User
import uuid

class Submission(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hackathon = models.ForeignKey(Hackathon, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    summary = models.CharField(max_length=255)
    details = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "submissions"
        verbose_name = "Submission"
        verbose_name_plural = "Submissions"

    def __str__(self):
        return "Submission - {user_id} - {hackathon_id})".format(
            user_id=self.user.user_id,
            hackathon_id=self.hackathon.id,
        )