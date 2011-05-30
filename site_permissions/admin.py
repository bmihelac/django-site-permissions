from django.contrib import admin
from django.contrib.sites.models import Site
from guardian.admin import GuardedModelAdmin


class SiteAdmin(GuardedModelAdmin):
    pass

admin.site.unregister(Site)
admin.site.register(Site, SiteAdmin)

