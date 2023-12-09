from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class BoardPost(models.Model):
    image = models.ImageField(upload_to='user_uploads')
    content = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
