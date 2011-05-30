from django.db import models
from django.contrib.sites.models import Site


class Category(models.Model):
    site = models.ForeignKey(Site)
    name = models.CharField('name', max_length=100)

    def __unicode__(self):
        return self.name

