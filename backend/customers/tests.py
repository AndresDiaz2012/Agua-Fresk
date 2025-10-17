from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from customers.models import Customer


class CustomersApiTest(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='u', password='p', role='admin')
        res = self.client.post('/api/auth/token/', {'username': 'u', 'password': 'p'})
        self.token = res.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_create_and_list_customer(self):
        # create
        payload = {
            'full_name': 'Juan Perez',
            'address': 'Calle 123',
            'phone_e164': '+5215512345678',
            'is_active': True
        }
        res = self.client.post('/api/customers/', payload, format='json')
        self.assertEqual(res.status_code, 201, res.data)
        # list
        res = self.client.get('/api/customers/')
        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.data['count'] >= 1)
