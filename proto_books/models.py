from pyexpat import model
from re import T
from django.db import models
# Create your models here.

class BookmarkModel(models.Model):
    site_title = models.CharField(max_length=200)
    site_url = models.URLField()
    site_keyword = models.JSONField()
    site_memo = models.TextField(blank=True,null=True,max_length=1000,)
    COLOR_CHOICES = (
    (1, '🟥red'),
    (2, '🟦blue'),
    (3, '🟩green'),
    (4, '🟨yellow'),
    (5, '🟧orange'),
    (6, '⬛black'),
    (7, '⬜gray'),
    (8, '🟪purple')
    )
    site_color = models.IntegerField(choices=COLOR_CHOICES, default=2)
