from django.core.validators import MinLengthValidator
from django.db import models
from django.urls import reverse
from tinymce.models import  HTMLField

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
    attachment=models.FileField(upload_to='notifications/attachments',blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"

    def __str__(self):
        return self.message[:20].join("...")

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})



# Create your models here.
class EmailConfig(models.Model):
    from_email = models.EmailField(max_length=100)
    email_password = models.CharField(
        max_length=128, validators=[MinLengthValidator(8)])
    email_host = models.CharField(max_length=50, default="mail.tdbsoft.co.ke")
    email_port = models.CharField(max_length=5, default=465)
    use_tls = models.BooleanField(default=True)
    fail_silently = models.BooleanField(default=True)
    email_message_template=HTMLField(default="\
                                     Dear {County_Administrator_Name},I hope this email finds you well.\
                                    This is a notification to bring to your attention some missed opportunities that have been identified within our county's operations. Upon review of recent data and analysis, it has become apparent that certain areas have not been fully optimized, potentially resulting in lost efficiency and effectiveness.")

    # def save(self, *args, **kwargs):
    #     self.email_password = make_password(self.email_password)
    #     super(EmailConfig, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.from_email

    class Meta:
        verbose_name_plural = 'Email Configuration'
