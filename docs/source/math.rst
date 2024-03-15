.. default-role:: math


############
Introduction
############
The documentation for the Four package is littered with references to logical and mathematical concepts and terminology that are most likely pretty obscure to most. Although I do wonder just how true that is for anyone who would wind up here. I should probably give you more credit. Either way, I've done my best to explain these concepts and aggregate definitions alongside the package docs to serve as quick references.

Also, of the ten or so of you who may actually be interested in this topic, I suspect somewhere between seven and eight have a background heavier in mathematics than in programming (although I may be failing to account for where and how I plan on publishing this). I wanted to try to lay everything out (at least as best as I know how) in mathematical terms, not just from the perspective of a programmer. If I was willing to settle for that, I would have stopped at documenting my code and been done with it, or perhaps if that still didn't feel like enough, I might have just used some python-like notation or pseudo-code for everything.

Having said that though, I'll immediately buy it back a little. I'm a software engineer by trade, not a mathematician. I've never written a math paper. That's not my world. I'm sure that much will become abundantly clear. I've *borrowed* (you mathematicians can definitely have it back when I'm done butchering it) notation from a number of math disciplines that may or may not actually make sense once I'm done clumsily cobbling them together; set-theory, predicate logic, etc... I also don't have the first clue what to consider obvious or what level of detail to aim for, so even though I know you're probably more than capable of putting everything together with less, when in doubt, I've erred on the side of *more* detail.


##############
Number Anatomy
##############
Numbers aren't just collections of digits. While we are more likely to recognize a number by its digits, this isn't a number's only useful attribute. In fact, with no additional information, a sequence of digits alone does not sufficiently define a number. For example, either by context, convention, or explicit conveyance, to know what value a sequence of digits represents, we must first know the radix of the number, what base number system the digits belong to.

.. math:: 10 \overset{?}{=} 10


*************************
Number Digits and Radixes
*************************
It is true that in most contexts we would just assume a number is written in base-10 because that is the base number system we found most natural to use as a species. There are all sorts of explanations for that by the way, but I'm not an anthropologist either, so I won't speculate. The point is, you don't really *know* that 10 = 10 unless both numbers share a radix (are in the same base). It's common to see the radix displayed in subscript when it needs to be made explicit (ironically enough we still *assume* the radix is a base-10 number, but that's an assumption that has to make at some point).

.. math:: 10_{2} \ne 10_{10}

This is just one property of a number aside from its digits. In this context, there are some other (often less important) properties that I need to define clearly because I will reference them quite often moving forward.


.. _rebase:

`R_{b}(x)` : Rebasing a Number
==============================
Since we're on the topic, going forward it will be useful at times to define numbers with a radix of 1000. As far as conversions go, this may be one of the most natural base-conversions we can make, seeing as we already do this to some extent when we denote periods with commas. If we treat each period as a unique digit, converting from base-10 to base-1000 becomes as simple as grouping every three base-10 digits together and calling that a new digit. In fact, all number systems with a base that is a power of 10 are equally as easy to “convert” in the same way. More generally speaking, you can actually switch between number systems for which the bases are both a power of any shared base in a similar manor as long as you only use digits from the shared base. For example, 152341 in base-6 is the same as three base-36 digits with base-6 values 15, 23, and 41 or two base-216 digits with base-6 values 152 and 341, etc...

.. math:: 152341_{6} = (15,23,41)_{36} = (152,341)_{216}

As I've mentioned, I'm a software engineer by trade, so I have my share of experience converting between bases with powers of 2 this way, except we in the computer world tend to convert our digits when we get to base-16 (hexadecimal), where A-F are used as digits with values 10-15, respectively.

.. math:: 10110110_{2} = (10, 11, 01, 10)_{4} = (10, 110, 110)_{8} = (1011, 0110)_{16} = \text{B}6_{16}

However, since I don't feel like defining 984 more unique digits, when we convert between decimal (base-10) and base-1000, we'll stick with the comma-delimited decimal values to represent base-1000 digits.

.. math:: 123456789_{10} = (123,456,789)_{1000}

Let `R_{b}(x)` be defined as a generic function that takes any positive decimal integer `x` and returns a sequence of `(c, p)` 2-tuples where each `c` is the decimal value of a digit in base-`b` and `p` is the power of `b` for which `c` is the coefficient.

.. math::
    R_{b}\vert_{\mathbb{Z}^+}(x) = \Biggl(
        \left(
            \left\lfloor
                \frac{x}{b^{\lfloor \log_{b} x \rfloor - i}} \bmod b
            \right\rfloor,
            \lfloor \log_{b} x \rfloor - i
        \right)
    \Biggr)_{i=0}^{\lfloor \log_{b} x \rfloor}

While including the power explicitly alongside each digit is unnecessary, it will make defining functions based on rebased numbers easier later. Combining this with the example we used above would return something like this:

.. math:: R_{1000}(123456789) = \bigl( (123, 2), (456, 1), (789, 0) \bigr)


.. _period-list compression:

`P(x)` : Period-List Compression
================================
We aren't finished with this base-1000 notation though. Eventually, we will be dealing with some very highly *repetitive* numbers in base-1000. Not only will we rebase these, but we're going to think of them explicitly as sequences of `(v, r)` 2-tuples, where `v` is a period value (a base-1000 digit), and `r` is a number of times `v` repeats in place; again, both written as decimal values.

.. math:: (1,001,345,345,345,345,345,345,789)_{1000} = \bigl( (1, 2), (345, 6), (789, 1) \bigr)

We could represent this idea mathematically as a convoluted sum of repeating decimal products:

.. math:: (1,001,345,345,345,345,345,345,789)_{1000} = (.\overline{001})1000^{9} - (.\overline{001})1000^{7} + (.\overline{345})1000^{7} - (.\overline{345})1000^{1} + 789

For human readability though, I may prefer something like a vinculum_ with explicit `r` values to denote the finitude of each repetition.

.. math:: (1,001,345,345,345,345,345,345,789)_{1000} = \overset{_{2}}{\overline{001}},\overset{_{6}}{\overline{345}},789

However, this neither of these are very computer-readable. In the Four package, I compromised on a more hybrid representation that could be typed in-line when taking numbers as input strings and printing these numbers as output.

.. math:: (1,001,345,345,345,345,345,345,789)_{1000} = [001]\{2\}[345]\{6\}789

Ordinarily, writing numbers this way would be extremely inefficient. A couple major factors make this representation more effective. First, as I stated above, we will be dealing with highly repetitive numbers, so the overhead we introduce with this representation is negligible compared to the gains we get from compression at scale. Second, on top of their repetitiveness, the numbers we'll be working with are *inconceivably* large. While a seasoned mathematician might laugh at the notion of infinity, computers can't handle it. We need a way of compressing these highly repetitive numbers without *any* loss of precision if we want to eventually use our math to compute results.

Let `P(x)` be defined as the function which takes any positive decimal integer `x` and returns the appropriate sequence of `(v, r)` tuples representing `x` as a period-list compression.

.. math:: P\vert_{\mathbb{Z}^+}(x) = \left(
        \bigr( v_{m}, r_{m} \bigl)\
        \Bigg\vert\ v_{m} = c_{n} \land c_{n} \ne c_{n+1}
        \land r_{m} = \bigl\lvert R_{1000}(x) \bigr\rvert - p_{n} - \sum_{i=1}^{m-1} r_{i}
    \right)_{(c_{n}, p_{n}) \in R_{1000}(x)}


.. _digit-occurrences:

`O_{d, b}(a, z)` : Digit Occurrences
====================================
Unless you're into some super niche combinatorics, you've probably never tried counting the number of times a digit occurs between two integers. Better yet, even if you have, you likely haven't needed to do it in say base-42 or base-123 or anything other than decimal I would wager. Well, believe it or not, we're going to need a function that does this later. This one's a doozy, so we'll take it in steps, starting with a specific case and then iterating our way to the more desirable generic function. Let's say we want to know how many times the digit 5 occurs in all decimal integers within the interval `[0, 100)`. If we just list them out we might see some sort of pattern.

.. math::
    \underbrace{5, 15, 25, 35, 45,
        \overbrace{50, 51, 52, 53, 54, 55, 56, 57, 58, 59}^{\text{50's}},
    65, 75, 85, 95}_{\text{05's}}

You might notice you can group the occurrences by placement. That is to say, 5 occurs 10 times as the first digit (in all the numbers 50-59) and 10 more times as the second digit in all the numbers 5-95. The pattern is quantifiable. We can break this problem down by asking how many times a digit occurs in each available position. I.e. the answer is the sum of the occurrences of 5 in the units place (10) and the occurrences of 5 in the tens place (10).

Now, consider all the 5's between 0 and 1000. We would see 5 in the hundreds place 100 times for every 1000 integers, in the tens place 10 times every 100 integers and the units place 1 time every 10 integers. Let's rearrange these.

.. math::
    \underbrace{
        500, 501, \ldots, 598, 599
    }_{\lvert \text{500's} \rvert = 100}
    \
    \underbrace{
        \begin{matrix}
            50 & \cdots & 59 \\
            \vdots & \ddots & \vdots \\
            950 & \cdots & 959
        \end{matrix}
    }_{\lvert \text{050's} \rvert = 10 \times 10}
    \
    \underbrace{
        5, 15, \ldots, 985, 995
    }_{\lvert \text{005's} \rvert = 100}

Notice that some numbers will show up in multiple lists, those with multiple 5's. These duplicates are a good thing. It means they get counted a number of times equal to the number of 5's in them. That is how many lists they appear in. So if we simply take the magnitude of each of the original sequences, we'll get our answer.

.. math::
    \lvert \text{500's} \rvert
    + \lvert \text{050's} \rvert
    + \lvert \text{005's} \rvert = 300

Great! We've established a base pattern, but this is a really simple example. What happens when we pick a more complicated number; something more precise with respect to the base, i.e. a number that isn't a perfect power of the base we're counting in, say 5814? Well, let's try listing them again.

.. math::
    \underbrace{
        5000, 5001, \ldots, 5812, 5813
    }_{\lvert \text{5000's} \rvert = 814}
    \
    \underbrace{
        \begin{matrix}
            500 & \cdots & 599 \\
            \vdots & \ddots & \vdots \\
            5500 & \cdots & 5599
        \end{matrix}
    }_{\lvert \text{0500's} \rvert = 6 \times 100}
    \
    \underbrace{
        \begin{matrix}
            50 & \cdots & 59 \\
            \vdots & \ddots & \vdots \\
            5750 & \cdots & 5759
        \end{matrix}
    }_{\lvert \text{0050's} \rvert = 58 \times 10}
    \
    \underbrace{
        5, 15, \ldots, 5795, 5805
    }_{\lvert \text{0005's} \rvert = 581}

This is a more helpful example because it makes another pattern more apparent. The magnitude of each list or array can be described in terms of the digit 5 and powers of 10 (the base).

.. math::
    \lvert \text{5000's} \rvert & = 814
        = 10^{3} \left( \left\lfloor \frac{5814}{10^{4}} \right\rfloor \right) + (5814 \bmod 10^{3}) \\
    \lvert \text{0500's} \rvert & = 600
        = 10^{2} \left( \left\lfloor \frac{5814}{10^{3}} \right\rfloor + 1 \right) \\
    \lvert \text{0050's} \rvert & = 580
        = 10^{1} \left( \left\lfloor \frac{5814}{10^{2}} \right\rfloor \right) \\
    \lvert \text{0005's} \rvert & = 581
        = 10^{0} \left( \left\lfloor \frac{5814}{10^{1}} \right\rfloor \right)

There are three distinct cases to be aware of for each digit in our upper boundary. Each digit can either be (1) less than, (2) greater than, or (3) equal to 5. In our example for 5814, we can see the first case applies to the last two digits, the second case applies to the second digit, and the last case applies to the first digit.

This all looks suspiciously like the makings of a series, one we might be able to define as the sum of some expression for each digit in our number. If we use `R_{10}(x)` to retrieve the `(c, p)` pairs for each base-10 digit, we could then express this as a summation by attaching `Iverson brackets`_ to portions of the formula so that it can be uniformly applied to each digit while still respecting each case.

.. math::
    O\vert_{\mathbb{Z}^+}(5814) = \sum \Biggl(
        10^{p} \left(
            \left\lfloor \frac{5814}{10^{p+1}} \right\rfloor + [c > 5]
        \right)
        + (x \bmod 10^{p}) [c = 5]
    \Biggr)_{(c, p) \in R_{10}(5814)}

With this specific formula in hand, it shouldn't be too much of a leap to see how it can be generalized to describe a function `O_{d, b}\vert_{\mathbb{Z}^+}(z)` which counts the occurrences of *any* digit `d` in the desired base `b` between 0 and some limit `z`, assuming `d < b`.

.. math::
    O_{d, b}\vert_{\mathbb{Z}^+}(z) = \sum \biggl(
        b^{p} \left(
            \left\lfloor \frac{z}{b^{p+1}} \right\rfloor + [c > d]
        \right)
        + (z \bmod b^{p}) [c = d]
    \biggr)_{(c, p) \in R_{b}(z)}

One last thing this function doesn't yet account for is the special case where `d` is equal to 0. Leading 0's shouldn't be counted. So, regardless of the base, 0 will occur less often, proportional to the number of digits that are equal to 0 in `R_{b}(z)`. After we account for this we'll be close to the final product.

.. math::
    O_{d, b}\vert_{\mathbb{Z}^+}(z) = \sum \Biggl(
        b^{p} \left(
            \left\lfloor \frac{x}{b^{p+1}} \right\rfloor + [c > d] - [d = 0]
        \right)
        + (x \bmod b^{p}) [c = d]
    \Biggr)_{(c, p) \in R_{b}(x)} + [d = 0]

With this core function defined, it's now fairly easy to get occurrences between *any* two positive integers, not just 0 and `z`. Call this new starting point or lower boundary `a` and let `O_{d, b}\vert_{\mathbb{Z}}(a, z)` be a recursive, piecewise function that returns the number of times `d` occurs in all the base-`b` integers in the interval `[a, z)`. Notice we can expand the domain to include all integers so long as we provide cases for all possible permutations for the parodies of `a` and `z`.

.. math::
    O_{d, b}\vert_{\mathbb{Z}}(a, z) = \begin{cases}
        O_{d, b}\vert_{\mathbb{Z}}(\lvert z - 1 \rvert, \vert a - 1 \rvert) &
            \text{ if } a < z \le 0 & \\
        O_{d, b}\vert_{\mathbb{Z}}(1, \lvert a - 1 \rvert) + O_{d, b}\vert_{\mathbb{Z}^+}(z) &
            \text{ if } a < 0 < z & \\
        O_{d, b}\vert_{\mathbb{Z}^+}(z) - O_{d, b}\vert_{\mathbb{Z}^+}(a) &
            \text{ if } 0 \le a < z & \text{base case} \\
        0 & \text{ if } a \ge z \lor d \ge b & \text{base case}
    \end{cases}


*************************
Number Names and Numerals
*************************
When I reference a number's name, what I am referring to specifically is the number's English `short scale`_ spelling according to the `Conway-Wechsler System`_ conceived by John Conway and Alan Wechsler and published in *The Book of Numbers* by John Conway and Richard Guy. All number names by this definition are comprised of one to many numerals. Loosely speaking, the word numeral can be used to refer to any representation of a number, but in this context, I use numeral in the linguistic sense to reference a specific set of English words. Each numeral falls into one of two distinct categories: period value numerals, or period name numerals.


.. _period value numerals:

Period Value Numerals
=====================
Period value numerals are the finite set of English words that may be combined to convey the value of any number in the interval `[1, 1000)`:

    one, two, three, four, five, six, seven, eight, nine, ten, eleven, twelve, thirteen, fourteen, fifteen, sixteen, seventeen, eighteen, nineteen, twenty, thirty, forty, fifty, sixty, seventy, eighty, ninety, hundred

NATURAL_NUMBERS_LT_1000_ defines all 1000 of these numerals with one exception, an empty string as the zeroth element.


.. _period name numerals:

Period Name Numerals
====================
Period name numerals on the other hand are the infinite set of numerals that convey the *magnitude* of a period value as generated by the Conway-Wechsler naming system. That is, the set of unique numerals that label each period value in a number's name:

    thousand, million, billion, trillion, quadrillion, quintillion, *etc...*

ZILLION_PERIOD_PREFIXES_ defines the first 1000 prefixes for these names with one exception, *n* as the zeroth element.


.. _zillion:

******************************
`Z(x)` : Period Zillion Values
******************************
In the Conway-Wechsler naming system, the magnitude or zillion value (sometimes also called a base-illion value) is the basis of the method used to generate unique names for each period; the period name numerals we just talked about. The zillion value for any number, `x`, is just two less than the number of periods in `x`. More precisely though, it is equal to one less than the floored `\log_{1000}` of `x`.

.. math:: Z(x) = \bigl\lfloor \log_{1000}\ x \bigr\rfloor - 1


*******************************
`L(x)` : The Length of a Number
*******************************
I imagine if I asked most people to measure the *length* of a number with no additional context, the most common response I'd get would be a confused look. Herein, I will often refer to the length of numbers. This is a shorthand of sorts. More specifically, what I mean by the length of `x` or `L(x)` is The *number of letters* in `x`'s name, but that can be a mouthful, especially while simultaneously trying to incorporate that into more complex descriptions or equations, so I've adopted this linguistic shortcut.


In Terms of `S(x)` / The Easy Way
=================================
Imagine a function `S(x)`, which returns the Conway-Wechsler name/spelling as a sequence of English characters for any number `x`. When I wrote conwech, I called this function `number2text`_. Here I'll stick with `S(x)`. Also, let `A` be the set of all letters in the English alphabet.

.. math:: A = \{\text{a, b, c,} \ldots \text{, x, y, z}\}

Given `A` and a function like `S(x)`, one fairly straightforward method for finding the length of a number as I've defined it would be to simply spell it, remove any non-letter characters (like dashes and spaces), and then measure the length of the remaining sequence.

.. math:: L(x) = \left\lvert (c \mid c \in A)_{c \in S(x)} \right\rvert

This is fine from a purely mathematical perspective where time and resources are practically meaningless, but in the real world this is terribly inefficient for a computer to calculate at scale. Besides, the cool math is the efficient stuff. We can do better.


As The Sum of `L_{V}(x)` and `L_{N}(x)`
=======================================
All number names are just sequences of numerals with a specific structure. We can exploit that structure to our advantage. Every number name is really just a combination of smaller number names; one for each period in the number. While each of these names represent numbers in their own right, when we stick them together what we're actually doing is expressing their sum.

.. math::
    123,000,000: & \text{ one hundred twenty-three million} & & \\
    456,000: & & \text{ four hundred fifty-six thousand} & \\
    789: & & & \text{ seven hundred eighty-nine}

Additionally, each of these smaller names, like all other number names, can be split into its period value numerals and its period name numerals. If we're simply counting letters, then the order they appear in the name is unimportant, meaning we can express `L(x)` as a sum of two sub-functions.

.. math:: L(x) = L_{V}(x) + L_{N}(x)

Where `L_{V}(x)` and `L_{N}(x)` return the total number of letters in all the period value numerals and period name numerals in `x`, respectively.

.. math::
    L_{V}(123456789) = 62 \\
    L_{N}(123456789) = 15 \\
    L(123456789) = 77

So how can we define these functions *efficiently*?


`L_{V}(x)` : Period Value Letters
---------------------------------
In order to define `L_{V}(x)`, we can first define a useful sequence. Drawing on what we know about period value numerals, let's define a sequence `V` such that indexing it gives us the length of the index. Note that `V`'s indexes are `zero-based`_.

.. math::
    V = \Bigl(
        \left\lvert (c \mid c \in A)_{c \in S(x)} \right\rvert \times [x > 0]
    \Bigr)_{x=0}^{999}

We can do this because there are a finite number of period value numerals. Computationally, it is more efficient at larger scales to spell all of these once, count their letters, and then store their lengths at the appropriate index so that they can be retrieved any number of times without recalculation. `L_{V}(x)` can be defined as the sum of `V` indexed by each period value in `x`.

.. math::
    L_{V}(x) = \sum_{z=0}^{\left\lfloor \log_{1000} x \right\rfloor}
    V_{\left(\left\lfloor \frac{x}{1000^{z}} \right\rfloor \bmod 1000 \right)}

In fact, while the equation above is sufficient, we can actually simplify this by first converting `x` into a period-list compression as we defined them earlier using `P(x)` and then adding together the product of `V_{v}` and `r` for every `(v, r)` period-repetition.

.. math:: L_V(x) = \sum \bigl( V_v \times r \bigr)_{(v, r) \in P(x)}


`L_{N}(x)` : Period Name Letters
--------------------------------
This here is the tricky bit. Because there are an infinite number of unique periods, it may seem as if we are stuck spelling all of the period names for any given `x`. Spoiler alert: we're not, but we need to think outside the box a little.

At the core of the `Conway-Wechsler System`_ is a table of prefixes that, when combined, create a composite prefix if you will for any period name based on it's zillion value. However, this table is obviously finite. Using the method described by the system, we can only generate 999 unique period names before we exhaust the table. In order to generate an infinite number of unique period names, the system recycles the table. For periods with zillion values greater than 999 we do this by breaking the zillion value itself into periods, creating a list of composite prefixes from the table for each period value in the zillion. With the addition of a special nilli prefix to represent zillion periods with a value of 0, we now have exactly 1000 unique composite prefixes (we're ignoring thousand for now as a special case). We can do something similar to what we did with period value numerals (for efficiency at scale) and spell all of these period names once, count their letters, and then store their lengths at the appropriate index so that they can be retrieved any number of times without recalculation. We'll call this sequence `N`. Note that `N`'s indexes are also `zero-based`_.

.. math::
    N = \Bigl(
        \left\lvert (c \mid c \in A)_{c \in S(1000^{x+1})} \right\rvert - 5 - [x = 0]
    \Bigr)_{x=0}^{999}

Notice too that since we're using `S(x)` to define `N`, and we only want the length of the composite prefix, we subtract 5 to account for the length of one before each period name and the trailing on at the end of each prefix. We also subtract 1 from the zeroth element to account for the difference in length between *thousand* and *nillion*. Now, for the epiphany (hopefully). We have a set of 1000 unique things. Each of these unique things is used to represent a value in a number system. So what do we really have here?

.. centered:: Digits! We have digits!

Each of these composite prefixes is no more than a unique digit in a base-1000 number system. As an example, take the number 10\ :sup:`370370370`. The zillion value for this number is 123456789, and the Conway-Wechsler name for this number is *one tresviginticentillisesquinquagintaquadringentillinovemoctogintaseptingentillion*. We can see the relationship clearly by breaking the name down into each of it's composite prefixes.

.. math::
    10^{370370370} = \text{one }\
        \underbrace{\text{tresviginticentilli}}_{123}\
        \underbrace{\text{sesquinquagintaquadringentilli}}_{456}\
        \underbrace{\text{novemoctogintaseptingentilli}}_{789}\
    \text{on}

This means the number of letters attributable to period names in any given number `x` can be expressed in terms of `N`, `Z(x)`, and `O_{d,1000}(a, z)` for all digits, `d`, in `[0, 1000)`.

.. math::
    L_{N}(x) = 2Z(x) + 1
    + \sum_{d=0}^{999} N_{d} \times O_{d,1000}(0, Z(x))

Before the sum, we add 2 times the zillion value to account for the *on* at the end of the each period name. We also and add back 1 extra letter for the difference between *nillion* and *thousand*. However, there's still one issue we need to address. When a period value is 0, we don't include the period name in that number's spelling. This summation is only correct for numbers that have no 0-periods. We can account for it by subtracting the lengths of those missing periods from the total. This is easier done when `x` is a period-list compression. First though, we'll generalize `L_{N}(x)` similar to how we did `O_{d,b}(x)` by defining `L_{Z}` as a function of some starting point, `a`, and some limit, `z`, and say that `L_{Z}(a, z)` returns the number of letters attributable to period names for all periods with zillion values within the interval `[a, z)`.

.. math::
    L_{Z}(a, z) = 2\bigl( z - a[a > 0] \bigr) + [a \le 0 < z]
    + \sum_{d=0}^{999} N_{d} \times O_{d,1000}(a, z)

Now, we can refine our definition of `L_{N}` in terms of `Z`, `P`, and `L_{Z}`, completing everything we need to finalize our definition of `L(x)`. We no longer have to spell a number to know exactly how long it is.

.. math::
    L_{N}(x) = L_{Z}(0, Z(x)) - \sum \left(
        L_{Z}(z - r_{n}, z)\
        \Bigg\vert\
        v_{n} = 0 \land z = Z(x) - \sum_{i=1}^{n-1} r_{i}
    \right)_{(v_{n}, r_{n}) \in P(x)}


################
4-Chain Concepts
################
As Matt describes them in his video, 4-chains are sequences of numbers for which each element is equal to the length of the previous element. We can represent this rather succinctly with a `recurrence relation`_:

.. math:: x_{n+1} = L(x_{n})

By this measure, the sequence I defined at the beginning of my developer's note is an incomplete 4-chain. The complete chain would look something like this:

.. math:: 123,456,789 \to 77 \to 12 \to 6 \to 3 \to 5 \to 4

Matt tasked his viewers with finding longer 4-chains. If `L(x)` had a proper inverse this wouldn't be very difficult. Instead of our recurrence relation defining `x_{n+1}` in terms of `L(x_{n})`, we could use `L^{-1}(x_{n})`.

.. math:: x_{n+1} = L^{-1}(x_{n})

This would effectively reverse all 4-chains, causing them to iterate upward to infinity. Our example above would then look something like this:

.. math:: 4 \to 5 \to 3 \to 6 \to 12 \to 77 \to 123,456,789 \to \cdots

However, even though every number's name is *necessarily* unique, *no* number's name has a unique *length*. This means `L(x)` is a many-to-one function; a surjection_, but not an injection_, and thus *not* a bijection_, meaning it is *not* invertible. `L^{-1}(x)` is in fact a multifunction_, which (despite the misnomer) really isn't a *function* in the strictest sense, meaning neither too is `x_{n+1}` as a function of *only* `x_{n}`. We may be able to define `x_{n+1}` in other terms though. In fact we'll still reverse the order. We just won't change the method.

.. math:: x_{n-1} = L(x_{n})


****************************
`C` : 4-Chain Index Notation
****************************
Going forward it would be nice to have a standard notation by which we can quickly reference any 4-chain, whether we know it's members or not. What other properties of a 4-chain can we draw upon to identify it? In his video, Matt tried finding the longest 4-chain he could. To do that, he first computed the 4-chain for every number up to 100 and then just picked the longest of those with the smallest starting number, or we might prefer to say (more generically) its first *unique* member.


4-Chains Ordered by Their Values
================================
We can draw on that intuition to formally define a collection of all 4-chains as a sequence, where each member chain is ordered in turn by its first unique element.

.. math:: C = \bigl( x_{m,n-1} = L(x_{m,n}) \bigr)_{m \in \mathbb{Z}^{+}}

Hopefully, since we aren't defining a function, a recurrence relation should be sufficient to get the point across. We've dropped in our reversal of the original relation so that chains appear in the desired order, meaning their first unique element is their *last* element. If we represent 4-chains this way we end up with a sequence of sequences like:

.. math::
    C = \bigl(
        (4, 0), (4, 5, 3, 1), (4, 5, 3, 2), (4, 5, 3),
        (4), (4, 5), (4, 5, 3, 6), (4, 5, 7), \ldots
    \bigr)

This is a start, but it still seems chaotic. We still can't really consistently discern valuable information about any 4-chain `C_{n}` from its notation, which is the point.


4-Chains Grouped by Their Length
================================
If we take this organization just a little further, we'll get what we want. Imagine now that all 4-chains in `C` are grouped by their length. This adds another dimension to our sequence. Call these new groupings of 4-chains sequences as well, and within `C`, order them by the length of the 4-chains they contain. Assuming I haven't butchered the notation too much, `C` can now be defined as follows:

.. math:: C = \bigl(x_{l,m,n-1} = L(x_{l,m,n}) \mid l = n \bigr)_{(l, m) \in \mathbb{N}^{2}}

With this definition, `C` becomes almost function-like. And, just in case I *have* butchered this notation, a good example might clear things up. Indexing `C` like `C_{4,3,2}` gives the 2\ :sup:`nd` number of the 3\ :sup:`rd` 4-chain that is 4 numbers long:

.. math::
    C = \Bigl(
        \bigl( (4) \bigr),
        \bigl( (4, 0),(4, 5),(4, 9) \bigr),
        \bigl( (4, 5, 3), (4, 5, 7), (4, 5, 8), (4, 9, 17), \ldots \bigr),
        \bigl( (4, 5, 3, 1), (4, 5, 3, 2), (4, 5, 3, 6) \ldots \bigr),
    \ldots\Bigr)
.. math::
    C_{4} = \bigl(
        (4, 5, 3, 1), (4, 5, 3, 2), (4, 5, 3, 6), (4, 5, 3, 10), (4, 5, 7, 15),
    \ldots\bigr)
.. math:: C_{4,3} = (4, 5, 3, 6)
.. math:: C_{4,3,2} = 5

Also, note that `C` is indexed from 1, not 0. While zero-indexing made more sense above, it does not here, where (1) there are no 0-length chains, and (2) I'll more likely refer to chains or their elements as the first, second, third, etc... Here, natural numbers seem more... natural.


**************************
`T` : Aggregating 4-Chains
**************************
Why stop at one supertask_ though? In some ways it may be more helpful if we can visualize `C` as a more searchable structure. We can also use this same relation to define a graph. More specifically, we can define *the 4-Tree* or `T` as the infinite `ordered tree`_ of all `(x, L(x))` pairs such that `x` is a positive integer:

.. math:: T = \bigl\{ (x, L(x)) \mid x \in \mathbb{Z}^+ \bigr\}
.. graphviz:: 4-tree-100.gv

We can clearly see that every 4-chain is simply a traversal from a given starting point to the root (4) of the 4-Tree. Right away, you might notice the three vertices 0, 1, and 2. If we could graph all of `T`, we would see that these vertices are the only vertices with a degree of 1. This is because every number's name is at least three letters long. I.e. There are *no* numbers with names shorter than three letters.

.. math::
    \forall x \in \mathbb{Z}^+, L(x) \ge 3
    \equiv
    \nexists x \in \mathbb{Z}^+, L(x) \lt 3

If `T` is an out-tree or arborescence_, these vertices are dead ends. Alternatively, if `T` is an in-tree or anti-arborescence these vertices are unreachable. I will sometimes refer to these as sterile numbers.


************************
The Case for `C` and `T`
************************
So why exactly did we go to all this trouble defining and redefining infinite triple-nested sequences and a never-ending polytree? Well, I wanted the rest of this to go a little smother, especially since I'm going to start blending math and pseudo-code. `C` and `T` are both powerful conceptual tools. I'll use `C` to reference specific chains in terms of their `C` indices as I did earlier in the example above, and `T` will be useful from an algorithmic perspective when we start searching for specific 4-chains.


#################
Hunting for 8 & 9
#################
Congrats! You've made it to the home stretch. Matt asked his viewers to find the first 4-chain with 8 members in it (`C_{8,1}` using our new notation), and we finally have most of the tools we need to start searching. There are a few more odds and ends to cover first though.


**************************
Letter-Inefficient Numbers
**************************

.. container:: right-floating

    .. table::
        :align: left

        +-------------+-----------------------------+--------+
        | `x`         | `S(x)`                      | `L(x)` |
        +===+=========+==============+==============+========+
        | 1 | 6\ [1]_ | one          | six          | 3      |
        +---+---------+--------------+--------------+--------+
        | 0 | 4\ [1]_ | zero         | four         | 4      |
        +---+---------+--------------+--------------+--------+
        | 3           | three                       | 5      |
        +-------------+-----------------------------+--------+
        | 11          | eleven                      | 6      |
        +-------------+-----------------------------+--------+
        | 15          | fifteen                     | 7      |
        +-------------+-----------------------------+--------+
        | 13          | thirteen                    | 8      |
        +-------------+-----------------------------+--------+
        | 17          | seventeen                   | 9      |
        +-------------+-----------------------------+--------+
        | 24          | twenty-four                 | 10     |
        +-------------+-----------------------------+--------+
        | 23          | twenty-three                | 11     |
        +-------------+-----------------------------+--------+
        | 73          | seventy-three               | 12     |
        +-------------+-----------------------------+--------+
        | 101         | one hundred one             | 13     |
        +-------------+-----------------------------+--------+
        | 104         | one hundred four            | 14     |
        +-------------+-----------------------------+--------+
        | 103         | one hundred three           | 15     |
        +-------------+-----------------------------+--------+
        | 111         | one hundred eleven          | 16     |
        +-------------+-----------------------------+--------+
        | 115         | one hundred fifteen         | 17     |
        +-------------+-----------------------------+--------+
        | 113         | one hundred thirteen        | 18     |
        +-------------+-----------------------------+--------+
        | 117         | one hundred seventeen       | 19     |
        +-------------+-----------------------------+--------+
        | 124         | one hundred twenty-four     | 20     |
        +-------------+-----------------------------+--------+
        | 123         | one hundred twenty-three    | 21     |
        +-------------+-----------------------------+--------+
        | 173         | one hundred seventy-three   | 22     |
        +-------------+-----------------------------+--------+
        | 323         | three hundred twenty-three  | 23     |
        +-------------+-----------------------------+--------+
        | 373         | three hundred seventy-three | 24     |
        +-------------+-----------------------------+--------+

    .. [1] Although 6 and 4 are not LINs as we've defined them strictly, it is useful to include them here as they are the *most* letter-inefficient numbers of their respective lengths that are not also *sterile* numbers.

Let's talk about efficiency for a second. Consider the ratio `x : L(x)` for every positive integer `x`. Imagine we grouped all of these ratios by their denominator, `L(x)`. In every group, there would be some minimum for which `x` is what I like to refer to as a letter-inefficient number or LIN. They use more letters with respect to their value than any other number of their length.

Put another way, LINs are the first occurring positive integers of any particular length; the minimum `x` for each natural number `n` such that `L(x) = n`. Due to the nature of English numerals, the set of all LINs ordered by `L(x)` is also only *approximately* ordered by `x`. There are a finite number of exceptions, but they are important. All of them occur within the set of LINs less than 1000 (table on right).

The LINs 4, 15, 24, 104, 115, and 124 all come before 3, 13, 23, 103, 113, and 123 respectively. Wherever it shows up, it seems the numerals for 3 are abnormally long for its value.


***************************
Letter-Inefficient 4-Chains
***************************
Notice that all of the numbers in `C_{5,1}` appear in the table (when we account for sterile numbers). This makes sense. The first occurring 4-chain of any length `l` will always be comprised entirely of LINs (and/or 4 and 6). This is due to the fact that the first occurring 4-chain of any length `l` is merely a continuation of the first occurring 4-chain of length `l-1` with exceptions made for 4-chains ending with sterile numbers, `C_{2,1}` and `C_{4,1}`.

.. math::
    C_{l,1} = \begin{cases}
        (4, 3, 5), & \text{if}\ l = 3 \\
        (4, 3, 5, 6, 11), & \text{if}\ l = 5 \\
        C_{l-1,1} + (C_{l,1,l}), & \text{otherwise}
    \end{cases}

You might then call 4-chains like `C_{l,1}` letter-inefficient chains or LICs. These LICs are the only 4-chains we’re currently interested in, meaning the only numbers we need to check in our search are a limited subset of LINs. If we can generate LINs, then we can generate LICs.


****************************
`F(l_{t})` : Generating LINs
****************************
Finally, it's time for some algorithms. We're going to define a function `F(l_{t})` that finds the first number (LIN) of the given target length `l_{t}`. It may help to begin by thinking of how we might generate LINs in order. To do that, we're going to break the first few LINs into their building blocks.

Similar to how we label every period with a period name, we have conventions that label every digit in a period. The only problem is that these conventions are inconsistent. We don't call 111 *one hundred one ten one unit*. No, like the first period, the units place has no name. We just say *one*. However, that's not the biggest problem with this system. English is messy. The main issue is derived from how we express double digit numbers. Because of this, it's easier to think of period values as `mixed radix`_ numbers in this context.

.. math:: 111 = 1_{10}11_{100}

When we consider numerals associated with either of these new digits separately, we can isolate some new LIN building blocks. The tens are a bit tricky and there are some patterns we could more thoroughly examine, but it's not too much to just check these exhaustively. We'll exclude *zero* and *six* here because neither will appear anywhere after `F(3)` and `F(4)`, respectively. The hundreds mimic the single digit LINs because they are based directly on the decimal digits, the only difference being the name *hundred* tacked on to the end of each and the absence of a *zero hundred* all together. What we end up with is a subset of the digits for both positions in our mixed radix system from above.

.. container:: left-floating

    .. table::
        :align: right

        +---------------+---------------+--------+
        | Base-10 Digit | Numeral       | Length |
        +===============+===============+========+
        | 1             | one hundred   | 3      |
        +---------------+---------------+--------+
        | 3             | three hundred | 5      |
        +---------------+---------------+--------+

    .. table::
        :align: right

        +----------------+---------------+--------+
        | Base-100 Digit | Numeral       | Length |
        +================+===============+========+
        | 1              | one           | 3      |
        +----------------+---------------+--------+
        | 4              | four          | 4      |
        +----------------+---------------+--------+
        | 3              | three         | 5      |
        +----------------+---------------+--------+
        | 11             | eleven        | 6      |
        +----------------+---------------+--------+
        | 15             | fifteen       | 7      |
        +----------------+---------------+--------+
        | 13             | thirteen      | 8      |
        +----------------+---------------+--------+
        | 17             | seventeen     | 9      |
        +----------------+---------------+--------+
        | 24             | twenty-four   | 10     |
        +----------------+---------------+--------+
        | 23             | twenty-three  | 11     |
        +----------------+---------------+--------+
        | 73             | seventy-three | 12     |
        +----------------+---------------+--------+

Notice, we'll also exclude *four (hundred)* because there is no case where we will prefer it over *three hundred*, and this highlights a core aspect of LIN generation.

Consider the case of 323 and 473. Despite being the same length, `F(23)` is 323 because 323 is less than 473, and therefore has a smaller `x : L(x)` ratio. So, when finding the LIN that comes after 173, we don't simply take the next base-10 digit LIN from the table (4) and append the same base-100 digit LIN (73). We prioritize the smaller value and roll back the base-100 digit accordingly to account for any extra letters added by the more significant base-10 digit.

More generally speaking, when generating LINs iteratively, every time we add a more significant digit to produce the next LIN, we will prioritize the smallest possible value for that digit, but only if we are able to compensate by adjusting less significant digits. This happens to be the only time this occurs in this context (LINs under 1000), but we will encounter similar behavior later on as we define the method for generating much larger LINs.

So let's consider the other end of the problem space now and think big. If we need to know an arbitrarily large LIN, `x`, what would be the quickest way to at least *estimate* it? If we can define a process for reliably iterating between LINs *and* we can define an efficient method for estimating LINs to within an iterable distance, then we'll be in business.

To start, we know that 373 is the largest LIN under 1000, meaning it's the largest *period value* LIN. Any LIN with a length greater than 24 will require more than one period. Additionally, beyond a certain threshold, as `x` goes to infinity the ratio of period value letters to period name letters goes to zero:

.. math:: \lim_{x \to \infty} \frac{L_{V}(x)}{L_{N}(x)} = 0

This is important because it tells us that (most of the time at least) an overwhelming majority of the letters in a number's name will come from its period name numerals. This threshold by the way seems to be in the *decillibillibillibillions* (1000\ :sup:`10002002003`). *Decillibillibillibillion* is the last Conway-Wechsler period name that has 24 or fewer letters in it. Thus, adding any period of greater magnitude will *always* result in adding more period name letters than period value letters. Anyway, I digress...

The fastest way to a minimal value estimate would be to find the smallest number of periods our target number *must* have. For any target length `l_{t}` we might begin by searching only numbers consisting of periods with the value 373. We can call this sequence of estimates `E`.

.. math:: E = \Bigl( \overset{_{n}}{\overline{373}} \Bigr)_{n \in \mathbb{N}} = \left( \lfloor 0.\overline{373} \times 1000^{n} \rfloor \right)_{n \in \mathbb{N}} = (373, 373373, 373373373, \ldots)

The goal here is actually pretty simple. Until we find a number longer than our target length, `l_{t}`, we want to maximize the number of letters we add with each period (not skipping any) while minimizing each period value. Mathematically, we could do this iteratively, but it's much more efficient to use some variation of `exponential search`_. We search until we find `n` such that the following inequality is true:

.. math:: L\bigl(E_{n-1}\bigr) \lt l_{t} \le L\bigl(E_{n}\bigr)

Given `L(x) = l_{t}`, when the above inequality is true, then the following must also be true:

.. math:: E_{n-1} \lt x \le E_{n}

So, once we find `n`, we know `x` must be one of exactly `373 \times 1000^{n}` integers in the interval `\bigl(E_{n-1}, E_{n}\bigr]`.

That's still a lot of numbers; in almost all cases, still too many to search exhaustively. If at this point `L(E_{n}) = l_{t}`, then we've won a hyper-cosmic scale lottery and need do nothing more; `x = E_{n}`. However, in the slightly more likely event that `l_{t} \lt E_{n}`, then we can remove letters by converting some number, `m`, of the most significant 373 periods to 001. Each period we convert in this way removes 21 letters from our total length; 21 being the difference in length between *three hundred seventy-three* and *one*. Therefore, we can determine exactly how many leading periods we must convert:

.. math:: m = \left\lceil \frac{L(E_{n}) - l_{t}}{21} \right\rceil

With `m` in hand, we can define a number that is guaranteed to have a length within 21 letters of `l_{t}`:

.. math:: l_{t} - 21 \lt L(\overset{_{m}}{\overline{001}},\overset{_{n-m}}{\overline{373}}) \le l_{t}

We have but one step left from here. We must make up the difference in length (whatever it is) by modifying the last 001 period value (and potentially the first 373 period value). Our target LIN, `x`, must take the following form:

.. math:: x = \overset{_{m-1}}{\overline{001}},\overset{_{1}}{\overline{y}},\overset{_{1}}{\overline{z}},\overset{_{n-m-1}}{\overline{373}}

There are only so many possibilities in this problem space. It would be trivial for a modern computer, but we can do the work once and create a table mapping each offset/difference, `d`, to it's corresponding `y` & `z` values, both of which come from a subset of the LIN periods in our previous table.

.. table::
    :align: center

    +------------------------------------------------------------------------------+-----+-----+-----------------------------+-----------------------------+---------------+
    | `l_{t} - L(\overset{_{m}}{\overline{001}},\overset{_{n-m}}{\overline{373}})` | `y` | `z` | `S(y)`                      | `S(z)`                      | `L(y) + L(z)` |
    +==============================================================================+=====+=====+=============================+=============================+===============+
    | 1                                                                            | 003 | 323 | three                       | three hundred twenty-three  | 28            |
    +------------------------------------------------------------------------------+-----+-----+-----------------------------+-----------------------------+---------------+
    | 2                                                                            | 003 | 373 | three                       | three hundred seventy-three | 29            |
    +------------------------------------------------------------------------------+-----+-----+-----------------------------+-----------------------------+---------------+
    | 3                                                                            | 011 | 373 | eleven                      | three hundred seventy-three | 30            |
    +------------------------------------------------------------------------------+-----+-----+-----------------------------+-----------------------------+---------------+
    | 4                                                                            | 013 | 323 | thirteen                    | three hundred twenty-three  | 31            |
    +------------------------------------------------------------------------------+-----+-----+-----------------------------+-----------------------------+---------------+
    | 5                                                                            | 013 | 373 | thirteen                    | three hundred seventy-three | 32            |
    +------------------------------------------------------------------------------+-----+-----+-----------------------------+-----------------------------+---------------+
    | 6                                                                            | 017 | 373 | seventeen                   | three hundred seventy-three | 33            |
    +------------------------------------------------------------------------------+-----+-----+-----------------------------+-----------------------------+---------------+
    | 7                                                                            | 023 | 323 | twenty-three                | three hundred twenty-three  | 34            |
    +------------------------------------------------------------------------------+-----+-----+-----------------------------+-----------------------------+---------------+
    | 8                                                                            | 023 | 373 | twenty-three                | three hundred seventy-three | 35            |
    +------------------------------------------------------------------------------+-----+-----+-----------------------------+-----------------------------+---------------+
    | 9                                                                            | 073 | 373 | seventy-three               | three hundred seventy-three | 36            |
    +------------------------------------------------------------------------------+-----+-----+-----------------------------+-----------------------------+---------------+
    | 10                                                                           | 101 | 373 | one hundred one             | three hundred seventy-three | 37            |
    +------------------------------------------------------------------------------+-----+-----+-----------------------------+-----------------------------+---------------+
    | 11                                                                           | 103 | 323 | one hundred three           | three hundred twenty-three  | 38            |
    +------------------------------------------------------------------------------+-----+-----+-----------------------------+-----------------------------+---------------+
    | 12                                                                           | 103 | 373 | one hundred three           | three hundred seventy-three | 39            |
    +------------------------------------------------------------------------------+-----+-----+-----------------------------+-----------------------------+---------------+
    | 13                                                                           | 111 | 373 | one hundred eleven          | three hundred seventy-three | 40            |
    +------------------------------------------------------------------------------+-----+-----+-----------------------------+-----------------------------+---------------+
    | 14                                                                           | 113 | 323 | one hundred thirteen        | three hundred twenty-three  | 41            |
    +------------------------------------------------------------------------------+-----+-----+-----------------------------+-----------------------------+---------------+
    | 15                                                                           | 113 | 373 | one hundred thirteen        | three hundred seventy-three | 42            |
    +------------------------------------------------------------------------------+-----+-----+-----------------------------+-----------------------------+---------------+
    | 16                                                                           | 117 | 373 | one hundred seventeen       | three hundred seventy-three | 43            |
    +------------------------------------------------------------------------------+-----+-----+-----------------------------+-----------------------------+---------------+
    | 17                                                                           | 123 | 323 | one hundred twenty-three    | three hundred twenty-three  | 44            |
    +------------------------------------------------------------------------------+-----+-----+-----------------------------+-----------------------------+---------------+
    | 18                                                                           | 123 | 373 | one hundred twenty-three    | three hundred seventy-three | 45            |
    +------------------------------------------------------------------------------+-----+-----+-----------------------------+-----------------------------+---------------+
    | 19                                                                           | 173 | 373 | one hundred seventy-three   | three hundred seventy-three | 46            |
    +------------------------------------------------------------------------------+-----+-----+-----------------------------+-----------------------------+---------------+
    | 20                                                                           | 323 | 373 | three hundred twenty-three  | three hundred seventy-three | 47            |
    +------------------------------------------------------------------------------+-----+-----+-----------------------------+-----------------------------+---------------+
    | 21                                                                           | 373 | 373 | three hundred seventy-three | three hundred seventy-three | 48            |
    +------------------------------------------------------------------------------+-----+-----+-----------------------------+-----------------------------+---------------+

And that's it... That's all we need to know in order to generate any LIN, and subsequently (given enough time and resources), we could generate any 4-chain, `C_{n,1}`. So what is `C_{8,1}`?


*******************************
`C_{8,1}` : The Manual Exercise
*******************************
Using everything we've covered to this point, we can walk through the generation of `C_{8,1}` as an example. Given only the chain Matt provided us in his video, `C_{6,1} = (4, 5, 3, 6, 11, 23)`, we can first find `C_{7,1}` by combining what we know about LICs with our table of LINs under 1000:

.. math::

    C_{7,1} &= C_{6,1} + (C_{7,1,7}) \\
            &= C_{6,1} + \bigl(F(C_{6,1,6})\bigr) \\
            &= \bigl(4, 5, 3, 6, 11, 23, F(23)\bigr) \\
            &= \bigl(4, 5, 3, 6, 11, 23, 323\bigr) \\

With `C_{7, 1}` in hand, we can search for `C_{8,1}` by following our process above with `l_{t} = L(C_{8,1,8}) = 323`:

.. math::

    C_{8,1} = \bigl(4, 5, 3, 6, 11, 23, 323 &, F(323)\bigr) \\
    \\
    L\bigl(\overset{_{0}}{\overline{373}}\bigr) = 0 \lt 323 &\gt L\bigl(\overset{_{1}}{\overline{373}}\bigr) = 24 \\
    L\bigl(\overset{_{1}}{\overline{373}}\bigr) = 24 \lt 323 &\gt L\bigl(\overset{_{2}}{\overline{373}}\bigr) = 56 \\
    L\bigl(\overset{_{2}}{\overline{373}}\bigr) = 56 \lt 323 &\gt L\bigl(\overset{_{4}}{\overline{373}}\bigr) = 118 \\
    L\bigl(\overset{_{4}}{\overline{373}}\bigr) = 118 \lt 323 &\gt L\bigl(\overset{_{8}}{\overline{373}}\bigr) = 254 \\
    L\bigl(\overset{_{8}}{\overline{373}}\bigr) = 254 \lt 323 &\lt L\bigl(\overset{_{16}}{\overline{373}}\bigr) = 535 \\
    \\
    L\bigl(\overset{_{8}}{\overline{373}}\bigr) = 254 \lt 323 &\lt L\bigl(\overset{_{12}}{\overline{373}}\bigr) = 387 \\
    L\bigl(\overset{_{10}}{\overline{373}}\bigr) = 321 \lt 323 &\lt L\bigl(\overset{_{12}}{\overline{373}}\bigr) = 387 \\
    L\bigl(\overset{_{10}}{\overline{373}}\bigr) = 321 \lt 323 &\lt L\bigl(\overset{_{11}}{\overline{373}}\bigr) = 354 \\
    \\
    323 &\gt L\bigl(\overset{_{2}}{\overline{001}},\!\overset{_{9}}{\overline{373}}\bigr) = 312 \gt 302 \\
    323 &= L\bigl(\overset{_{1}}{\overline{001}},\!\overset{_{1}}{\overline{103}},\!\overset{_{1}}{\overline{323}},\!\overset{_{8}}{\overline{373}}\bigr) \\
    F(323&) = 1103323\overset{_{8}}{\overline{373}} \\
    \\
    C_{8,1} = \bigl(4, 5, 3, 6, 11, 23, 323 &, 1103323\overset{_{8}}{\overline{373}}\bigr) \\
    \\


***********************************
`C_{9,1}` : Efficiency With Silicon
***********************************
Repeating this process manually for `C_{9,1}` would take far too long. Thankfully, it's not outside the realm of computation just yet. We're talking about finding a number with over a *nonillion* letters in it's name. So this is where this pseudo-paper of mine comes to an end. There's just not much to say, other than that I wrote some code to do this for us and found `C_{9,1}`. That is of course assuming I made no mistakes. The best I can do is present you with the result:

.. math:: C_{9,1} = \bigl(4, 5, 3, 6, 11, 23, 323, 1103323\overset{_{8}}{\overline{373}}, \overset{_{5}}{\overline{001}}103323\overset{_{x}}{\overline{373}}\bigr), \text{where}\ x = 4664040982447497675590741019

This number can also be expressed another way:

.. math:: C_{9,1,9} = 1.001001001001103323 \times 1000^{4664040982447497675590741025} + \sum_{i=0}^{4664040982447497675590741018} 373 \times 1000^{i}

To offer a bit of perspective, the general consensus in the scientific community seems to be that there are somewhere between one quinquavigintillion (`10^{78}`) and one sesvigintillion (`10^{82}`) atoms in the observable universe. The name of `C_{9,1,9}` *begins* with *one quadrilliquattuorsexagintasescentilliquadragintilliduooctogintanongentilliseptenquadragintaquadringentilliseptenonagintaquadringentilli-quinquaseptuagintasescentillinonagintaquingentilliunquadragintaseptingentilliquinquavigintillion ...*

.. _mixed radix: https://en.wikipedia.org/wiki/Mixed_radix

.. misc. notation terms
.. _supertask: https://en.wikipedia.org/wiki/Supertask
.. _vinculum: https://en.wikipedia.org/wiki/Vinculum_(symbol)
.. _Iverson brackets: https://en.wikipedia.org/wiki/Iverson_bracket
.. _zero-based: https://en.wikipedia.org/wiki/Zero-based_numbering
.. _recurrence relation: https://en.wikipedia.org/wiki/Recurrence_relation
.. _ordered tree: https://en.wikipedia.org/wiki/Tree_(graph_theory)#Ordered_tree
.. _arborescence: https://en.wikipedia.org/wiki/Arborescence_(graph_theory)
.. _exponential search: https://en.wikipedia.org/wiki/Exponential_search

.. function notation terms
.. _bijection: https://en.wikipedia.org/wiki/Bijection
.. _injection: https://en.wikipedia.org/wiki/Injective_function
.. _surjection: https://en.wikipedia.org/wiki/Surjective_function
.. _multifunction: https://en.wikipedia.org/wiki/Multivalued_function
.. _deterministic: https://en.wikipedia.org/wiki/Deterministic_system

.. number naming terms
.. _short scale: https://simple.wikipedia.org/wiki/Long_and_short_scales#Short_scale
.. _Conway-Wechsler System: https://www.mrob.com/pub/math/largenum.html#conway-wechsler

.. conwech links
.. _number2text: https://kcaturner.github.io/conwech/docs/latest/package/conwech.functions.html#conwech.functions.number2text
.. _NATURAL_NUMBERS_LT_1000: https://kcaturner.github.io/conwech/docs/latest/package/conwech.lexicon.html#conwech.lexicon.NATURAL_NUMBERS_LT_1000
.. _ZILLION_PERIOD_PREFIXES: https://kcaturner.github.io/conwech/docs/latest/package/conwech.lexicon.html#conwech.lexicon.ZILLION_PERIOD_PREFIXES
