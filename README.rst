================
Site permissions
================

`Site permissions` django application allows restricting access to objects
based on sites. Basic goal is to allow restricting managing site content
to users and groups in django admin interface.

`Sites permissions` will add custom permission ``change_site_content`` to
``Site`` model. It depends on django-guardian.
Requiremenents
--------------

* django-guardian

* Django 1.2 or later

Configuration
-------------

Add ``site_permissions`` to INSTALLED_APPS::

    INSTALLED_APPS = (
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        # Uncomment the next line to enable the admin:
        'django.contrib.admin',
        # Uncomment the next line to enable admin documentation:
        # 'django.contrib.admindocs',

        'guardian',
        'site_permissions',
    )


In settings.py add authentication backends for guardian and site_permissions::

    AUTHENTICATION_BACKENDS = [
        'django.contrib.auth.backends.ModelBackend', # default backend
        'guardian.backends.ObjectPermissionBackend', # guardian
        "site_permissions.backends.SitePermissionBackend", # site_permissions
    ]

    ANONYMOUS_USER_ID = -1 # required for guardian

Run ``syncdb`` to create permission for Site object::

    ./manage.py syncdb

This will create ``Can change site content`` permission that affect in which sites
specified user or group can edit contents.

Usage
-----

1. Add ``RestrictSiteMixin`` mixin to admin classes::

    from django.contrib import admin

    from site_permissions.auth_backends import RestrictSiteMixin

    from models import Category


    class CategoryAdmin(RestrictSiteMixin, admin.ModelAdmin):
        pass


    admin.site.register(Category, CategoryAdmin)


2. In django admin set permissions for every ``Site`` object.

Example app
-----------

To test application and get a feeling how it works::

    cd example
    ./manage.py syncdb && ./manage.py loaddata sample_data.json

Usernames are ``admin`` and ``user1``. Password for all users is ``password``.

TODO
----

* add admin helper to filter foreign relationships within site

* site field name should be configurable

* handle many to many relationship to sites
