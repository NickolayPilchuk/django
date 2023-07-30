from django.test import TestCase


class MyTest(TestCase):
    def test_idk(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)