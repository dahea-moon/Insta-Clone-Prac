from django.contrib import admin
from .models import Posting, Image, Comment

# Register your models here.
admin.site.register(Posting)
admin.site.register(Image)
admin.site.register(Comment)