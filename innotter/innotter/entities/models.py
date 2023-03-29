from django.db import models
from users.models import User

class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name
    

class Page(models.Model):
   name = models.CharField(max_length=80)
   uuid = models.CharField(max_length=30, unique=True)
   description = models.TextField()
   tags = models.ManyToManyField(Tag, related_name='pages')

   owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pages')
   followers = models.ManyToManyField(User, related_name='follows', blank=True)

   image = models.ImageField(null=True, blank=True, upload_to='pages_images')

   is_private = models.BooleanField(default=False)
   follow_requests = models.ManyToManyField(User, related_name='requests', blank=True)

   unblock_date = models.DateTimeField(null=True, blank=True)

   def __str__(self):
        return self.name




class Post(models.Model):
   page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='posts')
   content = models.CharField(max_length=180)

   reply_to = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, related_name='replies', blank=True)

   likes = models.ManyToManyField(User, blank=True)

   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)

   def __str__(self):
        return self.content


