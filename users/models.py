from django.db import models
import uuid

class User(models.Model):
    user_id = models.UUIDField(
        primary_key=True, db_column="user_id", default=uuid.uuid4, editable=False
    )
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "users"
        verbose_name = "App User"
        verbose_name_plural = "App Users"

    def __str__(self):
        return "{email} - {name} - ({user_id})".format(
            email=self.email,
            name=self.name,
            user_id=str(self.user_id),
        )