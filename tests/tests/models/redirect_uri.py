from django.test import TestCase
from doac.models import Client, RedirectUri


class TestRedirectUriModel(TestCase):

    def test_unicode(self):
        client = Client(name="Test Client", access_host="http://localhost/")
        client.save()

        uri = RedirectUri(client=client,
            url="http://localhost/redirect_endpoint")
        uri.save()

        self.assertEqual(unicode(uri), uri.url)
