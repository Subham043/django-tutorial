from datetime import date #date module
from django.utils.translation import gettext_lazy as _ #for post type
from django.core.exceptions import ValidationError #validation module
from django.contrib.auth.models import User #user model
from django.db import models #model module
from django.urls import reverse

# Create your models here.

class TimestampInfo(models.Model): #abstract class for timestamp
    created_at = models.DateTimeField(auto_now_add=True) #only on creation datetime is added
    updated_at = models.DateTimeField(auto_now=True) #on every modification datetime is added

    class Meta:
        abstract = True #declares the current class as abstract

class UnauthenticatedUserInfo(models.Model): #abstract class for user details
    name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(max_length=250, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        abstract = True #declares the current class as abstract

class Article(TimestampInfo): #extends timestamp info abstract class
    class PostType(models.TextChoices): #creation choices for select field
        FOR_KIDS = 'FOR_KIDS', _('Kids')
        FOR_ADULTS = 'FOR_ADULTS', _('Adults')

    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    article_for = models.CharField(max_length=50, choices=PostType.choices, default=PostType.FOR_ADULTS) #using the choices for the charfield
    banner = models.ImageField(upload_to='post_banners/%Y/%m/%d/')# file will be saved to MEDIA_ROOT/uploads/2015/01/30
    publish_on = models.DateField(default=date.today, blank=True) #using the date module here for default
    is_draft = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="articles") #using the user model here for author forign key

    def __str__(self):
        return self.title
    
    def clean_fields(self, exclude=None):
        super().clean_fields(exclude=exclude)
        if self.title == "hello":
            raise ValidationError({
                'title': ValidationError(_('Hello title not allowed.'), code='invalid'),
            })
        
    def get_absolute_url(self):
        return reverse('blogs:article_detail_view', kwargs={'pk': self.pk})

class Comment(UnauthenticatedUserInfo, TimestampInfo): #extends user info abstract class and timestamp info abstract class
    article = models.ForeignKey(Article, on_delete=models.SET_NULL, blank=True, null=True, related_name="comment") #related name for reverse relationship
    comment = models.TextField()
    approved_by_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.comment
    
class Reply(UnauthenticatedUserInfo, TimestampInfo): #extends user info abstract class and timestamp info abstract class
    comment = models.ForeignKey(Comment, on_delete=models.SET_NULL, blank=True, null=True, related_name="reply")
    reply = models.TextField()
    approved_by_admin = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "replies"

    def __str__(self):
        return self.reply