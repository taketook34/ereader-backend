from django.urls import reverse
from rest_framework.test import APITestCase


class TestSetUP(APITestCase):
    def setUp(self):
        self.list_url = reverse('list')
        return super().setUp()

    def tearDown(self):
        return super().tearDown()


