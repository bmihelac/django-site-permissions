from django.db import models
from django.contrib.contenttypes.models import ContentType
import django.contrib.sites.models
from django.contrib.sites.models import Site
from django.contrib.auth.models import Permission


def create_permissions(app, created_models, verbosity, **kwargs):
    if app is not django.contrib.sites.models:
        return

    ctype = ContentType.objects.get_for_model(Site)

    obj, created = Permission.objects.get_or_create(
            codename="change_site_content",
            content_type=ctype,
            defaults={'name': "Can change site content"})

    if created and verbosity >= 2:
        print "Adding permission change_site_content %s " % obj


models.signals.post_syncdb.connect(create_permissions,
    dispatch_uid = "sitepermissions.management.create_permissions")

