########
Glossary
########

.. glossary::

    period
        A group of three consecutive digits in a base-10 number, sometimes delimited by commas. Only the leading period of a number may be fewer than three digits. Any positive integer x can be expressed as a summation of its periods:

        .. math:: x = \sum_{p=0}^{\lfloor \log_{1000} x \rfloor} (x \mod 1000^{p+1}) - (x \mod 1000^{p})

    period value
        A positive integer within the interval [0, 1000) representing a period in a :term:`period-list compression`.

    period repetition
        The number of times a period value is repeated in a :term:`period-list compression` before the next period in the list or the end of the number.

    PLC
    period-list compression
        A positive integer represented as a sequence of (P, R) tuples, where P is a :term:`period value` and R is a :term:`period repetition`.

    number name
        One or more :term:`numerals` used to represent a number in English.

    numeral
    numerals
        Loosely speaking, the word “numeral” can be used to refer to any representation of a number, but in this context, "numeral" is used in the linguistic sense to reference a specific set of English words. Each numeral falls into one of two distinct categories: :term:`period value numerals`, or :term:`period name numerals`.

    period value numeral
    period value numerals
        Period value numerals are the finite set of English words that may be combined to convey the value of any number in the interval [1, 1000):

            one, two, three, four, five, six, seven, eight, nine, ten, eleven, twelve, thirteen, fourteen, fifteen, sixteen, seventeen, eighteen, nineteen, twenty, thirty, forty, fifty, sixty, seventy, eighty, ninety, hundred

    period name numeral
    period name numerals
        The infinite set of numerals enumerated by the :term:`Conway-Wechsler System`, used to convey the magnitude of a preceding :term:`period value numeral`. That is, the set of unique numerals that label each period value in a number name:

            thousand, million, billion, trillion, quadrillion, quintillion, *etc...*

    Conway-Wechsler
    Conway-Wechsler System
        todo...

    :math:`L(x)`
    number length
    length of a number
        todo...
