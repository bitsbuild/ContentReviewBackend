from django.db import models
import uuid
from django.core.validators import MinValueValidator,MaxValueValidator
from django.contrib.auth.models import User

class StreamingPlatform(models.Model):
    platform_id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    platform_name = models.CharField(max_length=70)
    platform_about = models.CharField(max_length=350)
    platform_url = models.URLField()
    platform_created = models.DateTimeField(auto_now_add=True,editable=False)
    platform_updated = models.DateTimeField(auto_now=True,editable=False)
    def __str__(self):
        return self.platform_name
    
class Artists(models.Model):
    artist_id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    artist_name = models.CharField(max_length=70)
    artist_about = models.CharField(max_length=350)
    artist_created = models.DateTimeField(auto_now_add=True,editable=False)
    artist_updated = models.DateTimeField(auto_now=True,editable=False)
    def __str__(self):
        return self.artist_name
    
class ContentDetails(models.Model):
    content_id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    content_name = models.CharField(max_length=70)
    content_description = models.CharField(max_length=350)
    content_released = models.BooleanField(default=True)
    content_created = models.DateTimeField(auto_now_add=True,editable=False)
    content_updated = models.DateTimeField(auto_now=True,editable=False)
    content_platform = models.ForeignKey(StreamingPlatform,on_delete=models.CASCADE,related_name="content")
    artists = models.ManyToManyField(Artists,related_name="content",blank=True)
    def __str__(self):
        return self.content_name
    
class ContentReviews(models.Model):
    review_user = models.ForeignKey(User,on_delete=models.CASCADE)
    review_id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    review_name = models.CharField(max_length=70)
    review_body = models.CharField(max_length=350)
    review_stars = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(5)])
    review_created = models.DateTimeField(auto_now_add=True,editable=False)
    review_updated = models.DateTimeField(auto_now=True,editable=False)
    review_movie = models.ForeignKey(ContentDetails,on_delete=models.CASCADE,related_name="reviews")
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields = ['review_user','review_movie'],
                name='one_review_per_user'
            )
        ]
    def __str__(self):
        return self.review_name
