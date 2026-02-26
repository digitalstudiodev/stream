from django.db import models
from django.utils import timezone
from users.models import User
from django.urls import reverse
from multiselectfield import MultiSelectField
from PIL import Image

TAG_OPTIONS = (
    ("Featured","Featured"),
    ("Data","Data"),
    ("Django","Django"),
    ("AR","AR"),
    ("VR","VR"),
    ("Database","Database"),
    ("Python","Python"),
    ("AWS","AWS"),
    ("Heroku","Heroku"),
    ("Git","Git"),
    ("Physics","Physics"),
    ("Science","Science"),
    ("Case-Studies","Case-Studies"),
)


class Post(models.Model):
    title = models.CharField(max_length=100, default="")
    preview = models.CharField(max_length=5000, default="")
    content = models.TextField(default="", verbose_name="Content", null=True, blank=True, help_text="You can also upload a .html file with the content. If both are provided, the .html file will be used.")
    content_html_file = models.FileField(upload_to="post_html_files/", null=True, blank=True, verbose_name="Content HTML File")
    date_posted = models.DateTimeField(default=timezone.now)
    read_time = models.IntegerField(default=5, verbose_name="Read Time", help_text="in minutes")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tag = MultiSelectField(max_length=100, choices=TAG_OPTIONS, default="Featured", null=False, blank=False, max_choices=4)
    featured_image = models.ImageField(default='default.png', upload_to='blog_pics', verbose_name="Featured Image")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post-detail', kwargs={'pk': self.pk})
    
    def get_shorten_preview(self):
        # returning the first 100 characters of the preview
        return str(self.preview)[0:100] + str(" ... ")


class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    unsubscribed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.email