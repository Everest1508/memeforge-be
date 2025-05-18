from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid

# Create your models here.
class MemeforgeUser(models.Model):
    email = models.EmailField(_("Email"), max_length=254,unique=True)
    x_account = models.CharField(_("X Profile"), max_length=50,null=True,blank=True)
    profile_picture = models.URLField(null=True,blank=True)

    def __str__(self):
        return self.email
    



class UserTabiPayCardOverlay(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(MemeforgeUser, on_delete=models.CASCADE, related_name='tabipay_overlays', null=True)
    card = models.ForeignKey("featured.TabiPayCard", on_delete=models.CASCADE, related_name='user_overlays')
    
    username_text = models.CharField(max_length=100)
    name_text = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} on {self.card.title}"