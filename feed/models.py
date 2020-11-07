import unidecode 
from datetime import datetime
from django.db import models
from django.db.models.base import Model
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from tinymce.models import HTMLField
# Defines the status as published or draft


STATUS = (
    (0, 'Draft'),
    (1, 'Publish')
)

class Like(models.Model):
    users = models.ManyToManyField(User, related_name='requirement_comment_likes')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    created_on = models.DateTimeField(auto_now= True)
    class Meta:
        unique_together = ("content_type", "object_id")

class Comment(models.Model):
    author = models.ForeignKey(User,related_name="comments", on_delete=models.CASCADE)
    content = models.TextField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    created_on = models.DateTimeField(auto_now= True)
    like = GenericRelation(Like, related_query_name="like_for_comment")

class Post(models.Model):
    title = models.CharField(max_length= 200)
    slug = models.SlugField(max_length= 500, unique= True, allow_unicode=True)
    # If user is deleted the default value for author becomes "[deleted]"
    author = models.ForeignKey(User, on_delete=models.CASCADE, null= True)
    # RichTextField() is the field for ckeditor
    content = content = HTMLField()
    status = models.IntegerField(choices= STATUS, default= 0)
    created_on = models.DateTimeField(auto_now= True)
    updated_on = models.DateTimeField(auto_now= True)
    comments_enabled = models.BooleanField(default=True)
    comment = GenericRelation(Comment)
    like = GenericRelation(Like,related_query_name="like_for_post")

    class Meta:
        # The newly made post will be visible at the top
        ordering = ['-created_on']

    def save(self, *args, **kwargs):
        # creates a slug for the post on calling the save command
        now = datetime.now()
        self.slug = "%s_%s" %(slugify(unidecode.unidecode(self.title)),now.strftime("%m_%d_%Y_%H_%M_%S"))
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

class ImageTinymce(models.Model):
    image = models.ImageField()