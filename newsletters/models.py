from django.db import models
from django.contrib.auth.models import User
# Create your models here.




class NewsletterSubscription(models.Model):

    subscriber = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="subscriptions"
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="subscribers"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = (
            "subscriber",
            "author"
        )

    def __str__(self):
        return (
            f"{self.subscriber.username}"
            f" -> "
            f"{self.author.username}"
        )