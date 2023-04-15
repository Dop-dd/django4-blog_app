from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# canonical url
from django.urls import reverse


# part two: create a custom manager to retrieve all posts that have a PUBLISHED status.queryset.
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()\
                     .filter(status=Post.Status.PUBLISHED)

#1 part one: Create your models here.
class Post(models.Model):
    # 4. ad status for the post
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200,
                            unique_for_date='publish')
    #5. Adding a many-to-one relationship
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='blog_posts')
    body = models.TextField()
    # add time fiells
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2,
                                choices=Status.choices,
                                default=Status.DRAFT)
    # return queryset status
    objects = models.Manager() # the default manager
    published = PublishedManager() # our custom manager or query et

    # sort post in descending order
    class Meta:
        ordering = ['-publish']
        # improve query performance with an index
        indexes = [
                models.Index(fields=['-publish'])
        ]

    def __str__(self):
        return self.title

    # canonican url
    def get_absolute_url(self):
        # function will build the URL dynamically
        # id of the Post object as a positional argument by using self..
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])

