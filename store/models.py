from django.db import models
from django.shortcuts import reverse
from django.utils import timezone


class Item(models.Model):
    title = models.CharField(max_length=100, verbose_name="Item Name")
    price = models.FloatField(null = False, default=0)
    discount_price = models.FloatField(blank=True, null=True, verbose_name="Discounted Price")
    description = models.TextField(null=True, default=None)
    additional_info = models.TextField(null=True, default=None, verbose_name="Additional Information")
    featured_image = models.ImageField(blank=False, null=False, verbose_name="Featured Image", default="default.png", upload_to='item_pics')
    sub_image1 = models.ImageField(blank=False, null=False, verbose_name="Sub Image 1", default="default.png", upload_to='item_pics')
    sub_image2 = models.ImageField(blank=False, null=False, verbose_name="Sub Image 2", default="default.png", upload_to='item_pics')
    sub_image3 = models.ImageField(blank=False, null=False, verbose_name="Sub Image 3", default="default.png", upload_to='item_pics')
    sub_image4 = models.ImageField(blank=False, null=False, verbose_name="Sub Image 4", default="default.png", upload_to='item_pics')
    sub_image5 = models.ImageField(blank=False, null=False, verbose_name="Sub Image 5", default="default.png", upload_to='item_pics')
    inventory = models.FloatField(default=0)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("store:item-detail", kwargs={'pk': self.pk})