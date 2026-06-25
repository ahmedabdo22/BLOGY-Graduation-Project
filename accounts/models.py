from django.conf import settings
from django.db import models

class Profile(models.Model):
    ROLE_CHOICES = (
        ("reader", "Reader"),
        ("author", "Author"),
        ("admin", "Admin"),
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to="profiles/", blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="reader")
    dark_mode = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username,self.user.id} Profile"
