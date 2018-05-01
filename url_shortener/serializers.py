from rest_framework import serializers

from url_shortener.baseconv import base10to62
from url_shortener.models import ShortURL


class ShortURLSerializer(serializers.ModelSerializer):
    short_url = serializers.SerializerMethodField()

    def get_short_url(self, obj):
        return base10to62.from_decimal(obj.id)

    class Meta:
        model = ShortURL
        fields = ('short_url', 'url', 'date_submitted', 'usage_count')
        read_only_fields = ('date_submitted', 'usage_count')
