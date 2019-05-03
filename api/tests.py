from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User

# Create your tests here.
# Using the standard RequestFactory API to create a form POST request


class BasicTestCase(TestCase):
    def setUp(self):
        self.c = APIClient()
        self.user = User.objects.create_user(username='bipo', password='bipo')
        self.c.login(username='bipo', password='bipo')


    def test_new_reservierung_fail(self):
        response = self.c.post('/api/reservierung/', {'title': 'new reservierung'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_new_reservierung_ok(self):
        # Reservierung anlegen
        response = self.c.post('/api/reservierung/', {'kg': 4584, 'kunde':210 })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        BASE_URL = response.data['url']

        # add 4 Grundstücke
        res2 = self.c.post(BASE_URL+'add_gpkt/', {'kg': 56543, 'point_nums': 4 })
        self.assertEqual(len(res2.data['punkt_set']), 4)

        # check status of Reservation - must be in 'ANGELEGT'
        res3 = self.c.get(BASE_URL)
        self.assertEqual(res3.data['status'], 'A')

        # Reservierung löschen
        res4 = self.c.delete(BASE_URL)
        self.assertEqual(res4.status_code, status.HTTP_200_OK)

        
    def test_new_reservierung_deletegpkt(self):
        # Reservierung anlegen
        response = self.c.post('/api/reservierung/', {'kg': 4584, 'kunde':210 })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        BASE_URL = response.data['url']

        res2 = self.c.post(BASE_URL+'add_gpkt/', {'kg': 56543, 'point_nums': 4 })
        self.assertEqual(len(res2.data['punkt_set']), 4)

        res3 = self.c.put(BASE_URL+'set_progress/', {'kg': 56543, 'point_nums': 4 })
        self.assertEqual(res3.data['status'], 'B')

        res4 = self.c.delete(BASE_URL+'del_gpkt/', {'points': '14,35,56'})
        self.assertEqual(len(res4.data['punkt_set']), 4)

        res5 = self.c.delete(BASE_URL+'del_gpkt/', {'points': '1,2,3'})   
        self.assertEqual(len(res5.data['punkt_set']), 1)

        # Reservierung updaten
        res7 = self.c.put(BASE_URL, {'points':'5,6', 'kg': 4567})
        self.assertEqual(res7.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        res8 = self.c.patch(BASE_URL, {'points':'5,6', 'kg': 4567})
        self.assertEqual(res8.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        # Reservierung löschen
        res6 = self.c.delete(BASE_URL)
        self.assertEqual(res6.status_code, status.HTTP_400_BAD_REQUEST)

        res9 = self.c.put(BASE_URL+'set_done/')
        self.assertEqual(res9.status_code, status.HTTP_200_OK)
        