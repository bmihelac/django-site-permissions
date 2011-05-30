from django.contrib.sites.models import Site

from guardian.shortcuts import get_objects_for_user


class SitePermissionBackend(object):
    supports_object_permissions = True
    supports_anonymous_user = False

    def authenticate(self, username, password):
        return None

    def user_sites(self, user):
        return get_objects_for_user(user,
                ('change_site_content',),
                Site)

    def has_perm(self, user_obj, perm, obj=None):
        if obj is None:
            return False
        try:
            perm = perm.split('.')[-1].split('_')[0]
        except IndexError:
            return False
        return obj.site in self.user_sites(user_obj)


class RestrictSiteMixin(object):

    def has_change_permission(self, request, obj=None):
        opts = self.opts
        return request.user.has_perm(
                opts.app_label + '.' + opts.get_change_permission(), obj)

    def has_delete_permission(self, request, obj=None):
        opts = self.opts
        return request.user.has_perm(opts.app_label + '.' +
                opts.get_delete_permission(), obj)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        Filter ``site`` field with sites in user sites.
        """
        if db_field.name == "site":
            kwargs["queryset"] = SitePermissionBackend().user_sites(
                    request.user)
        return super(RestrictSiteMixin,
                self).formfield_for_foreignkey(db_field, request, **kwargs)

    def queryset(self, request):
        """
        Filter queryset with objects that belongs to user sites.
        """
        qs = super(RestrictSiteMixin, self).queryset(request)
        qs = qs.filter(site__in=SitePermissionBackend().user_sites(request.user))
        return qs

