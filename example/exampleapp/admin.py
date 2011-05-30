from django.contrib import admin

from site_permissions.auth_backends import RestrictSiteMixin

from models import Category


class CategoryAdmin(RestrictSiteMixin, admin.ModelAdmin):
    pass


admin.site.register(Category, CategoryAdmin)

