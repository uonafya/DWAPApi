from django.db import models
from django.urls import reverse
# Create your models here.
from django.contrib.auth import get_user_model

User = get_user_model()


class Notifications(models.Model):
    created_by = models.ForeignKey(User,
                                   on_delete=models.CASCADE, related_name='users')
    notified_user = models.ForeignKey(User,
                                      on_delete=models.CASCADE, related_name='notified_users')
    message = models.TextField(
        max_length=2500, default="Hellow,Welcome to Data Alignment Solutions")
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"

    def __str__(self):
        return self.message[:20].join("...")

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})
