from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model



class Avatars(models.Model):
    user = models.ForeignKey(get_user_model(),on_delete=models.DO_NOTHING, null=True)
    avatar = models.ImageField(upload_to="avatars/", null=True)

class Bio(models.Model):
    user = models.ForeignKey(get_user_model(),on_delete=models.DO_NOTHING, null=True)
    bio = models.TextField(max_length=150)

    
class Posts(models.Model):
    username = models.CharField(max_length=20)
    user = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING, null=True)
    avatar = models.ImageField(upload_to="avatars/", null=True)
    post_text = models.TextField()

    def get_absolute_url(self):
        return reverse("post", kwargs={"username": self.username, "post_id": self.pk})
    
    
    class Meta:
        verbose_name_plural = "Posts"
    
    
class Menu(models.Model):
    name = models.TextField()
    link = models.TextField()

