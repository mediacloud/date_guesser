Date Guesser
============

|Build Status| |Coverage| 

A library to extract a publication date from a web page, along with a measure of the accuracy.
This was produced as a part of the `mediacloud project <https://mediacloud.org/>`_, in order to accurately extract dates from content. 

Quickstart
----------
The date guesser uses both the url and the html to work, and uses some heuristics to decide which of many possible dates might be the best one.

.. code-block:: python
    
    from date_guesser import DateGuesser, Accuracy
    
    guesser = DateGuesser()

    # Uses url slugs when available
    guess = guesser.guess_date(url='https://www.nytimes.com/2017/10/13/some_news.html',
                               html='<could be anything></could>')

    #  Returns a namedtuple with three fields
    guess.date      # datetime.datetime(2017, 10, 13, 0, 0, tzinfo=<UTC>)
    guess.accuracy  # Accuracy.DATE
    guess.method    # 'Found /2017/10/13/ in url'

In case there are two trustworthy sources of dates, :code:`date_guesser` prefers the more accurate one

.. code-block:: python
 
    html = '''                                                                     
        <html><head>                                                                   
        <meta property="article:published" itemprop="datePublished" content="2017-10-13T04:56:54-04:00" />         
        </head></html>'''
    guess = guesser.guess_date(url='https://www.nytimes.com/2017/10/some_news.html',
                               html=html)
    guess.date  # datetime.datetime(2017, 10, 13, 4, 56, 54, tzinfo=tzoffset(None, -14400))
    guess.accuracy is Accuracy.DATETIME  # True

But :code:`date_guesser` is not led astray by more accurate, less trustworthy sources of information

.. code-block:: python
 
    html = '''                                                                     
        <html><head>                                                                   
        <meta property="og:image" content="foo.com/2016/7/4/whatever.jpg"/>         
        </head></html>'''
    guess = guesser.guess_date(url='https://www.nytimes.com/2017/10/some_news.html',
                               html=html)
    guess.date  # datetime.datetime(2017, 10, 15, 0, 0, tzinfo=<UTC>)
    guess.accuracy is Accuracy.PARTIAL  # True   

Installation
------------

The library is not yet available on PyPI, so installation is via github only for now:

.. code-block:: bash

    pip install git+https://github.com/mitmedialab/date_guesser
                                                  
Performance
-----------
We benchmarked the accuracy against the wonderful :code:`newspaper` library, using one hundred urls gathered from each of four very different topics in the :code:`mediacloud` system. This includes blogs and news articles, as well as many urls that have no date (in which case a guess is marked correct only if it returns :code:`None`).  

Vaccines
^^^^^^^^

+---------+---------------+-----------+
|         | date_guesser  | newspaper |
+=========+===============+===========+
| 1 days  |      48       |   **57**  |
+---------+---------------+-----------+
| 7 days  |       51      |   **61**  |
+---------+---------------+-----------+
| 15 days |       53      |   **66**  |
+---------+---------------+-----------+

Aadhar Card in India
^^^^^^^^^^^^^^^^^^^^

+---------+---------------+-----------+
|         | date_guesser  | newspaper |
+=========+===============+===========+
| 1 days  |      44       |   **73**  |
+---------+---------------+-----------+
| 7 days  |       44      |   **74**  |
+---------+---------------+-----------+
| 15 days |       44      |   **74**  |
+---------+---------------+-----------+

Donald Trump in 2017
^^^^^^^^^^^^^^^^^^^^

+---------+---------------+-----------+
|         | date_guesser  | newspaper |
+=========+===============+===========+
| 1 days  |      60       |  **79**   |
+---------+---------------+-----------+
| 7 days  |       61      |  **83**   |
+---------+---------------+-----------+
| 15 days |       61      |  **85**   |
+---------+---------------+-----------+

Recipes for desserts and chocolate
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

+---------+---------------+-----------+
|         | date_guesser  | newspaper |
+=========+===============+===========+
| 1 days  |       65      |   **83**  |
+---------+---------------+-----------+
| 7 days  |       69      |   **85**  |
+---------+---------------+-----------+
| 15 days |       69      |   **87**  |
+---------+---------------+-----------+



.. |Build Status| image:: https://travis-ci.org/mitmedialab/date_guesser.png?branch=master
   :target: https://travis-ci.org/mitmedialab/date_guesser
.. |Coverage| image:: https://coveralls.io/repos/github/mitmedialab/date_guesser/badge.svg?branch=master
   :target: https://coveralls.io/github/mitmedialab/date_guesser?branch=master
