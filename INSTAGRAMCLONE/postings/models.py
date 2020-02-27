from django.db import models
from django.urls import reverse

# created랑 modified 만들어줌 (created_at, updated_at)
from django_extensions.db.models import TimeStampedModel

from django.contrib.auth import get_user_model

# pip install pillow pilkit django-imagkit // image 넣을 때 한 세트처럼 사용
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit

User = get_user_model()

class HashTag(TimeStampedModel):
    tags = models.CharField(max_length=20, unique=True)


class Posting(TimeStampedModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='postings')
    contents = models.CharField(max_length=140)
    hashtags = models.ManyToManyField(HashTag, blank=True, related_name='postings')
    like_users = models.ManyToManyField(User, related_name='like_posts')

    class Meta:
        ordering = ('-created',)
    
    def get_absolute_url(self):
        return reverse("postings:posting_detail", kwargs={"posting_id": self.pk})


class Image(models.Model):
    posting = models.ForeignKey(Posting, on_delete=models.CASCADE, related_name='images')
    file = ProcessedImageField(
        # 비율에 맞게 이미지 변형
        processors=[ResizeToFit(600, 600, mat_color=(45, 45, 45))],
        upload_to='postings/images',
        format='JPEG',
        options={'quality':90}
    )


class Comment(TimeStampedModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    posting = models.ForeignKey(Posting, on_delete=models.CASCADE)
    content = models.CharField(max_length=140)