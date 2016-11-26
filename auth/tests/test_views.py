from django.test import TestCase
from django.test import Client


class RegisterTestCase(TestCase):
    def test_register(self):
        c = Client()

        # on success redirects to /
        response = c.post('/accounts/register/', {
            'username': 'asdas',
            'password1': 'asdasdasd12',
            'password2': 'asdasdasd12'
            })
        self.assertRedirects(response, '/')

        # passwords don't match
        response = c.post('/accounts/register/', {
            'username': 'asdasdasd1',
            'password1': 'asdasdasd1',
            'password2': 'asdasdasd2'
            })
        self.assertEquals(response.status_code, 200)

        # username is empty
        response = c.post('/accounts/register/', {
            'username': '',
            'password1': 'asdasdasd12',
            'password2': 'asdasdasd12'
            })
        self.assertEquals(response.status_code, 200)

        # no password
        response = c.post('/accounts/register/', {
            'username': 'asdasdasd',
            'password1': '',
            'password2': ''
            })
        self.assertEquals(response.status_code, 200)

        # username and password are similar
        response = c.post('/accounts/register/', {
            'username': 'asdasdasd0',
            'password1': 'asdasdasd1',
            'password2': 'asdasdasd1'
            })
        self.assertEquals(response.status_code, 200)
