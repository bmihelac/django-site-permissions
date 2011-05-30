from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.contrib.auth.models import User, Permission
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from guardian.shortcuts import assign

from exampleapp.models import Category


class AdminTest(TestCase):

    def setUp(self):
        self.user_1 = User.objects.create_user('user1',
                'user1@example.com',
                'user1')
        self.user_1.is_staff = True
        self.user_1.save()
        ct = ContentType.objects.get_for_model(Category)
        for perm in Permission.objects.filter(content_type=ct):
            self.user_1.user_permissions.add(perm)
        self.site_1 = Site.objects.create(domain="site_1.example.com",
                name="site 1")
        self.site_2 = Site.objects.create(domain="site_2.example.com",
                name="site 2")
        assign('change_site_content', self.user_1, self.site_1)
        self.client = Client()
        self.client.login(username='user1', password='user1')

    def tearDown(self):
        self.client.logout()

    def test_01_see_only_objects_for_site_with_change_site_permission(self):
        Category.objects.create(site=self.site_1, name="category-1")
        Category.objects.create(site=self.site_2, name="category-2")
        url = reverse('admin:exampleapp_category_changelist') 
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("category-1", response.content)
        self.assertNotIn("category-2", response.content)

    def test_02_add_only_object_for_site_with_change_site_permission(self):
        url = reverse('admin:exampleapp_category_add') 
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(unicode(self.site_1), response.content)
        self.assertNotIn(unicode(self.site_2), response.content)

    def test_03_add_with_tampering_site_data_should_fail(self):
        url = reverse('admin:exampleapp_category_add')
        response = self.client.post(url,
                data={'name': 'name', 'site': self.site_2.id})
        self.assertIn('That choice is not one of the available choices.',
                response.content)
