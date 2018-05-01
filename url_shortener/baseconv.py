#!/usr/bin/env python

"""
Numeric base conversion utility classes.

Sample usage:

Decimal to binary
>>> decimal_binary = DecimalBaseConverter(BASE2)
>>> decimal_binary.from_decimal(555)
'1000101011'

Binary to decimal
>>> decimal_binary.to_decimal('1000101011')
555

Integer interpreted as binary and converted to decimal
>>> decimal_binary.to_decimal(1000101011)
555

Decimal to base-4
>>> decimal_base4 = DecimalBaseConverter(BASE4)
>>> decimal_base4.from_decimal(99)
'1203'

Base-4 to base-5 (with alphabetic digits)
>>> base4_base5_alphabetic = BaseConverter(BASE4, BASE5_ALPHABETIC)
>>> base4_base5_alphabetic.convert(1203)
'dee'

...convert back
>>> base4_base5_alphabetic.reverse('dee')
'1203'

Base-5 (with alphabetic digits) back to base-10
>>> base5_alphabetic_base10 = BaseConverter(BASE5_ALPHABETIC, BASE10)
>>> base5_alphabetic_base10.convert('dee')
'99'

Decimal to a base that uses A-Z0-9a-z for its digits
>>> decimal_base62 = DecimalBaseConverter(BASE62)
>>> decimal_base62.from_decimal(257938572394)
'E78Lxik'

..convert back
>>> decimal_base62.to_decimal('E78Lxik')
257938572394

Binary to a base with words for digits (the function cannot convert this back)
>>> binary_to_words_base = BaseConverter(BASE2, ('Zero', 'One'))
>>> binary_to_words_base.convert('1101')
'OneOneZeroOne'
"""


BASE2 = "01"
BASE4 = "0123"
BASE5_ALPHABETIC = "abcde"
BASE10 = "0123456789"
BASE16 = "0123456789ABCDEF"
BASE62 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyz"


class BaseConverter(object):
    """
    Convert decimal numbers to any base-X number and back again.

    Based on: http://www.djangosnippets.org/snippets/1431/
    """

    def __init__(self, source_digits, target_digits):
        self.source_digits = source_digits
        self.target_digits = target_digits

    def convert(self, number):
        return BaseConverter._convert(number, self.source_digits, self.target_digits)

    def reverse(self, number):
        return BaseConverter._convert(number, self.target_digits, self.source_digits)

    @staticmethod
    def _convert(number, fromdigits, todigits):
        """
        Converts a "number" between two bases of arbitrary digits.

        The input number is assumed to be a string of digits from the
        'fromdigits' string (which is in order of smallest to largest digit).
        The return value is a string of elements from 'todigits'
        (ordered in the same way). The input and output bases are
        determined from the lengths of the digit strings. Negative
        signs are passed through.

        Based on: http://code.activestate.com/recipes/111286/
        """

        if str(number)[0] == '-':
            number, neg = str(number)[1:], 1
        else:
            neg = 0

        # Make an integer out of the number
        x = 0

        for digit in str(number):
            x = x * len(fromdigits) + fromdigits.index(digit)

        # Create the result in base 'len(todigits)'
        if x == 0:
            res = todigits[0]
        else:
            res = ''

            while x > 0:
                x, digit = divmod(x, len(todigits))
                res = todigits[digit] + res

            if neg:
                res = '-' + res

        return res


class DecimalBaseConverter(BaseConverter):
    """
    Convert decimal numbers to any base-X number and back again.

    Based on: http://www.djangosnippets.org/snippets/1431/
    """
    def __init__(self, todigits):
        super(DecimalBaseConverter, self).__init__(BASE10, todigits)

    def from_decimal(self, i):
        return self.convert(i)

    def to_decimal(self, s):
        return int(self.reverse(s))


base10to62 = DecimalBaseConverter(BASE62)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
