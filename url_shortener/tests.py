import pytest

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from url_shortener.baseconv import base10to62
from url_shortener.models import ShortURL
from url_shortener.serializers import ShortURLSerializer


pytestmark = pytest.mark.django_db


class ShortURLTests(APITestCase):
    def test_create_short_url(self):
        """
        Ensure we can create a new short URL object
        and that the response data matches the current object instance.
        """
        # Create a short URL
        url = reverse('shorturl-list')
        data = {'url': 'https://en.wikipedia.org/wiki/Test-driven_development'}
        response = self.client.post(url, data, format='json')
        # Verify response status
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Check if the number of short URL instances is one
        self.assertEqual(ShortURL.objects.count(), 1)
        # Retrieve the first (and only) short URL instance
        instance = ShortURL.objects.get()
        # Check if the 'url' attribute in the response data
        # matches the 'url' field of the model instance
        self.assertEqual(response.data['url'], instance.url)
        # Check if the 'short_url' attribute in the response data
        # matches the one computed by base 10 to base 62 converter
        self.assertEqual(response.data['short_url'], base10to62.from_decimal(instance.id))
        # Check if the 'usage_count' attribute in the response data is equal to 0
        self.assertEqual(response.data['usage_count'], 0)

    def test_forward_short_url(self):
        """
        Ensure a short URL call is permanently redirected to the original URL.
        """
        # Create a short URL
        url = reverse('shorturl-list')
        data = {'url': 'http://lkml.iu.edu/hypermail/linux/kernel/1510.3/02866.html'}
        response = self.client.post(url, data, format='json')
        short_url = response.data['short_url']

        # Call short URL
        url = reverse('shorturl-detail', args=[short_url])
        response = self.client.get(url)
        # Verify the response status code is a 301
        self.assertEqual(response.status_code, status.HTTP_301_MOVED_PERMANENTLY)
        # Verify the location header is set to the target URL
        self.assertEqual(response.get('location'), data['url'])

    def test_info_short_url(self):
        """
        Ensure the short URL info API response is the serialization of a short URL instance.
        """
        # Create a short URL
        url = reverse('shorturl-list')
        data = {'url': 'https://uwsgi-docs.readthedocs.io/en/latest/articles/TheArtOfGracefulReloading.html'}
        response = self.client.post(url, data, format='json')
        short_url = response.data['short_url']

        # Get short URL info
        url = reverse('shorturl-info', args=[short_url])
        response = self.client.get(url)

        # Retrieve the first (and only) short URL instance
        instance = ShortURL.objects.get()
        # Serialize the short URL instance
        serializer = ShortURLSerializer(instance)
        # Ensure the short URL info API response is equal to the serialized data
        self.assertEqual(response.data, serializer.data)

    def test_usage_count(self):
        """
        Ensure the usage count is increased at every call to a short URL.
        """
        # Create a short URL
        url = reverse('shorturl-list')
        data = {'url': 'https://docs.djangoproject.com/en/2.0/ref/urlresolvers/#reverse'}
        response = self.client.post(url, data, format='json')
        short_url = response.data['short_url']

        # Call short URL three times
        url = reverse('shorturl-detail', args=[short_url])
        self.client.get(url)
        self.client.get(url)
        self.client.get(url)

        # Get short URL info
        url = reverse('shorturl-info', args=[short_url])
        response = self.client.get(url)

        # Verify the current usage count is equal to 3
        self.assertEqual(response.data['usage_count'], 3)

    def test_duplicated_urls(self):
        """
        Ensure it's impossible to create two short URLs for the same original URL.
        """
        # Create a short URL
        url = reverse('shorturl-list')
        data = {'url': 'https://www.djangosnippets.org/snippets/1431/'}
        response = self.client.post(url, data, format='json')
        # Verify response status
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Create a short URL for the same URL
        response = self.client.post(url, data, format='json')
        # Verify response status
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
