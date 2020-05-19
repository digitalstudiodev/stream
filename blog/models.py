from django.db import models
from django.utils import timezone
from users.models import User
from django.urls import reverse
from multiselectfield import MultiSelectField
from PIL import Image

TAG_OPTIONS = (
    ("Featured","Featured"),
    ("AWS","AWS"),
    ("Python","Python"),
    ("Heroku","Heroku"),
    ("Bootstrap","Bootstrap"),
    ("Podcast","Podcast"),
    ("Workflow","Workflow"),
)


class Post(models.Model):
    title = models.CharField(max_length=100)
    preview = models.CharField(max_length=5000, default="")
    content = models.TextField(default="", verbose_name="Content")
    date_posted = models.DateTimeField(default=timezone.now)
    read_time = models.CharField(max_length=10, default="")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tag = models.CharField(max_length=100, choices=TAG_OPTIONS, default="Featured", null=False)
    featured_image = models.ImageField(default='default.png', upload_to='blog_pics', verbose_name="Featured Image")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
