################
Developer's Note
################

Wellcome to the bottom of the rabbit hole, fellow traveller!

Four started as a script I wrote to automate my search for the longest calculable 4-chain. What is a 4-chain you might ask... Well, if you enjoy those sequence puzzles we used to solve in math class then take a look at these numbers and try to figure out what comes next:

.. math:: 123,456,789 \to 77 \to 12 \to 6 \to 3 \to \ ?

Did you get? If you don't get it, don't worry. It's one of the most useless and obscure patterns in English numerals. I would've lived the rest of my life in blissful ignorance if not for Matt Parker's YouTube video_ about these. He does an excellent job explaining them, so instead of transcribing the video here, I'm just going to tell you to give it a watch. I'll save the break-downs for later.

Anyway, the script quickly grew in scope. I took a detour to write conwech_ (which also took on a life of its own) because I *thought* I needed the number-spelling package to end all number-spelling, at least for the English Short Scale, and I figured that maybe that portion of this work might find *some* practical use-case one day, though I still doubt it. At the end of the day, I used almost none of it, only a few members of the lexicon:

    - NATURAL_NUMBERS_LT_1000_
    - ZILLION_PERIOD_PREFIXES_

Eventually Four grew enough that I decided to make an effort to refactor the thing into a somewhat cohesive package, parameterizing, decoupling and organizing things into something I wasn't completely embarrassed to publish. Even if it never finds a practical application out in the wild (it won't), I think I just wanted to be able to say "I found it first." Ego... That's what this is. So without further adieu, here's my pseudo-paper/love letter to Matt Parker on the 4-chains he introduced me to.

.. toctree::
    :hidden:
    :caption: Math

    math.rst
    glossary.rst

.. toctree::
    :hidden:
    :caption: Code

    package.rst


Indices & Tables
================

* :ref:`Modules <modindex>`
* :ref:`Index <genindex>`
* `Static Analysis <.flake8/index.html>`_
* `Test Coverage <.coverage/index.html>`_

.. _video: https://www.youtube.com/watch?v=LYKn0yUTIU4
.. _conwech: https://kcaturner.github.io/conwech/docs/latest/
.. _NATURAL_NUMBERS_LT_1000: https://kcaturner.github.io/conwech/docs/latest/package/conwech.lexicon.html#conwech.lexicon.NATURAL_NUMBERS_LT_1000
.. _ZILLION_PERIOD_PREFIXES: https://kcaturner.github.io/conwech/docs/latest/package/conwech.lexicon.html#conwech.lexicon.ZILLION_PERIOD_PREFIXES
