from django.db import models

from url_shortener.baseconv import base10to62


class ShortURL(models.Model):
    """
    Model that represents a shortened URL
    """
    url = models.URLField(unique=True)
    date_submitted = models.DateTimeField(auto_now_add=True)
    usage_count = models.PositiveIntegerField(default=0)

    def __unicode__(self):
        return '{} : {}'.format(base10to62.from_decimal(self.id), self.url)

    class Meta:
        get_latest_by = 'date_submitted'
