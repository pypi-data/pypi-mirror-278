from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from aclvl_permissions.permissions import AccessLevelPermission

class AccessLevelPermissionTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.permission = AccessLevelPermission()

    def test_has_permission(self):
        request = self.factory.get('/some-url/')


    def test_has_object_permission(self):
        request = self.factory.get('/some-url/')
