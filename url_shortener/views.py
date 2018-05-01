from django.http import HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from url_shortener.baseconv import base10to62
from url_shortener.models import ShortURL
from url_shortener.serializers import ShortURLSerializer


class ShortURLViewSet(mixins.CreateModelMixin,
                      viewsets.GenericViewSet):
    """
    API endpoint that allows several actions against short URLs.
    """
    queryset = ShortURL.objects.all().order_by('-date_submitted')
    serializer_class = ShortURLSerializer

    def retrieve(self, request, *args, **kwargs):
        """
        Override the model instance retrieval method.
        Instead of building a standard response with the model instance,
        it redirects the short URL to the real, longer URL ('url' model field)
        it's linked to.
        Just before the redirection is performed the 'usage_count' model field
        is incremented.
        """
        instance = self.get_object()
        instance.usage_count += 1
        instance.save()
        return HttpResponsePermanentRedirect(instance.url)

    @action(methods=['get'], detail=True)
    def info(self, request, pk=None):
        """Bind the real retrieval action of a model instance."""

        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def get_object(self):
        """
        Override in order to retrieve by shorten URL string
        instead of internal ID.
        """
        queryset = self.get_queryset()

        # Interpret primary key as a short URL for convenient lookup
        obj = get_object_or_404(queryset, id=base10to62.to_decimal(self.kwargs['pk']))
        self.check_object_permissions(self.request, obj)

        return obj
