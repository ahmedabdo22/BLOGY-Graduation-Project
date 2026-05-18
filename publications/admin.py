from django.contrib import admin

# Register your models here.
from .models import (
    Publication,
    PublicationContributor,
    PublicationInvitation
)

admin.site.register(Publication)
admin.site.register(PublicationContributor)
admin.site.register(PublicationInvitation)