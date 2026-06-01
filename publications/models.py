from django.db import models
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

# Create your models here.
class Publication(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True , blank=True)
    description = models.TextField()
    logo = models.ImageField(upload_to='publications/logos/',blank=True,null=True)
    owner = models.ForeignKey(User,on_delete=models.CASCADE,related_name='owned_publications')
    created_at = models.DateTimeField(auto_now_add=True)
    delete_at = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class PublicationContributor(models.Model):
    ROLE_CHOICES = (
        ('owner', 'Owner'),
        ('editor', 'Editor'),
        ('writer', 'Writer'),
    )

    publication = models.ForeignKey(
        Publication,
        on_delete=models.CASCADE,
        related_name="contributors"   # ✅ add this
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='writer')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('publication', 'user')





class PublicationInvitation(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )

    publication = models.ForeignKey(
        Publication,
        on_delete=models.CASCADE,
        related_name='invitations'
    )

    invited_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='publication_invites'
    )

    invited_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_publication_invites'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.invited_user.username} -> {self.publication.name}"



def save(self, *args, **kwargs):

    if not self.slug:
        self.slug = slugify(self.name)