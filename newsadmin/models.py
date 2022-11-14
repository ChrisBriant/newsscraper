from django.db import models

# Create your models here.
class NewsItem(models.Model):
    source = models.CharField(max_length=30,null=False)
    headline = models.CharField(max_length=2550,null=False)
    link = models.CharField(max_length=1000,null=False)
    date_added = models.DateTimeField(auto_now_add=True)


#Contains persisted news items
class StoredNewsItem(models.Model):
    source = models.CharField(max_length=30,null=False)
    headline = models.CharField(max_length=2550,null=False)
    link = models.CharField(max_length=1000,null=False)
    date_added = models.DateTimeField(auto_now_add=True)