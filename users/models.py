from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class MemeforgeUser(models.Model):
    email = models.EmailField(_("Email"), max_length=254,unique=True)
    x_account = models.CharField(_("X Profile"), max_length=50)
    profile_picture = models.URLField(null=True)
