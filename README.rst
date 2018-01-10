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

.. raw:: html

    <h3>Vaccines</h3>
    <table id="T_3457ce06_f0f9_11e7_bb20_60f81dc9d130" > 
    <thead>    <tr> 
            <th class="blank level0" ></th> 
            <th class="col_heading level0 col0" >newspaper</th> 
            <th class="col_heading level0 col1" >date_guesser</th> 
        </tr></thead> 
    <tbody>    <tr> 
            <th id="T_3457ce06_f0f9_11e7_bb20_60f81dc9d130level0_row0" class="row_heading level0 row0" >1 days</th> 
            <td id="T_3457ce06_f0f9_11e7_bb20_60f81dc9d130row0_col0" class="data row0 col0" >48</td> 
            <td id="T_3457ce06_f0f9_11e7_bb20_60f81dc9d130row0_col1" class="data row0 col1" >57</td> 
        </tr>    <tr> 
            <th id="T_3457ce06_f0f9_11e7_bb20_60f81dc9d130level0_row1" class="row_heading level0 row1" >7 days</th> 
            <td id="T_3457ce06_f0f9_11e7_bb20_60f81dc9d130row1_col0" class="data row1 col0" >51</td> 
            <td id="T_3457ce06_f0f9_11e7_bb20_60f81dc9d130row1_col1" class="data row1 col1" >61</td> 
        </tr>    <tr> 
            <th id="T_3457ce06_f0f9_11e7_bb20_60f81dc9d130level0_row2" class="row_heading level0 row2" >15 days</th> 
            <td id="T_3457ce06_f0f9_11e7_bb20_60f81dc9d130row2_col0" class="data row2 col0" >53</td> 
            <td id="T_3457ce06_f0f9_11e7_bb20_60f81dc9d130row2_col1" class="data row2 col1" >66</td> 
        </tr></tbody> 
    </table> <h3>Aadhar Card in India</h3>
    <table id="T_3459bc5a_f0f9_11e7_8c42_60f81dc9d130" > 
    <thead>    <tr> 
            <th class="blank level0" ></th> 
            <th class="col_heading level0 col0" >newspaper</th> 
            <th class="col_heading level0 col1" >date_guesser</th> 
        </tr></thead> 
    <tbody>    <tr> 
            <th id="T_3459bc5a_f0f9_11e7_8c42_60f81dc9d130level0_row0" class="row_heading level0 row0" >1 days</th> 
            <td id="T_3459bc5a_f0f9_11e7_8c42_60f81dc9d130row0_col0" class="data row0 col0" >44</td> 
            <td id="T_3459bc5a_f0f9_11e7_8c42_60f81dc9d130row0_col1" class="data row0 col1" >73</td> 
        </tr>    <tr> 
            <th id="T_3459bc5a_f0f9_11e7_8c42_60f81dc9d130level0_row1" class="row_heading level0 row1" >7 days</th> 
            <td id="T_3459bc5a_f0f9_11e7_8c42_60f81dc9d130row1_col0" class="data row1 col0" >44</td> 
            <td id="T_3459bc5a_f0f9_11e7_8c42_60f81dc9d130row1_col1" class="data row1 col1" >74</td> 
        </tr>    <tr> 
            <th id="T_3459bc5a_f0f9_11e7_8c42_60f81dc9d130level0_row2" class="row_heading level0 row2" >15 days</th> 
            <td id="T_3459bc5a_f0f9_11e7_8c42_60f81dc9d130row2_col0" class="data row2 col0" >44</td> 
            <td id="T_3459bc5a_f0f9_11e7_8c42_60f81dc9d130row2_col1" class="data row2 col1" >74</td> 
        </tr></tbody> 
    </table> <h3>Donald Trump in 2017</h3>
    <table id="T_345b1de8_f0f9_11e7_99b2_60f81dc9d130" > 
    <thead>    <tr> 
            <th class="blank level0" ></th> 
            <th class="col_heading level0 col0" >newspaper</th> 
            <th class="col_heading level0 col1" >date_guesser</th> 
        </tr></thead> 
    <tbody>    <tr> 
            <th id="T_345b1de8_f0f9_11e7_99b2_60f81dc9d130level0_row0" class="row_heading level0 row0" >1 days</th> 
            <td id="T_345b1de8_f0f9_11e7_99b2_60f81dc9d130row0_col0" class="data row0 col0" >60</td> 
            <td id="T_345b1de8_f0f9_11e7_99b2_60f81dc9d130row0_col1" class="data row0 col1" >79</td> 
        </tr>    <tr> 
            <th id="T_345b1de8_f0f9_11e7_99b2_60f81dc9d130level0_row1" class="row_heading level0 row1" >7 days</th> 
            <td id="T_345b1de8_f0f9_11e7_99b2_60f81dc9d130row1_col0" class="data row1 col0" >61</td> 
            <td id="T_345b1de8_f0f9_11e7_99b2_60f81dc9d130row1_col1" class="data row1 col1" >83</td> 
        </tr>    <tr> 
            <th id="T_345b1de8_f0f9_11e7_99b2_60f81dc9d130level0_row2" class="row_heading level0 row2" >15 days</th> 
            <td id="T_345b1de8_f0f9_11e7_99b2_60f81dc9d130row2_col0" class="data row2 col0" >61</td> 
            <td id="T_345b1de8_f0f9_11e7_99b2_60f81dc9d130row2_col1" class="data row2 col1" >85</td> 
        </tr></tbody> 
    </table> <h3>Recipes for desserts and chocolate</h3>
    <table id="T_345ce952_f0f9_11e7_bd73_60f81dc9d130" > 
    <thead>    <tr> 
            <th class="blank level0" ></th> 
            <th class="col_heading level0 col0" >newspaper</th> 
            <th class="col_heading level0 col1" >date_guesser</th> 
        </tr></thead> 
    <tbody>    <tr> 
            <th id="T_345ce952_f0f9_11e7_bd73_60f81dc9d130level0_row0" class="row_heading level0 row0" >1 days</th> 
            <td id="T_345ce952_f0f9_11e7_bd73_60f81dc9d130row0_col0" class="data row0 col0" >65</td> 
            <td id="T_345ce952_f0f9_11e7_bd73_60f81dc9d130row0_col1" class="data row0 col1" >83</td> 
        </tr>    <tr> 
            <th id="T_345ce952_f0f9_11e7_bd73_60f81dc9d130level0_row1" class="row_heading level0 row1" >7 days</th> 
            <td id="T_345ce952_f0f9_11e7_bd73_60f81dc9d130row1_col0" class="data row1 col0" >69</td> 
            <td id="T_345ce952_f0f9_11e7_bd73_60f81dc9d130row1_col1" class="data row1 col1" >85</td> 
        </tr>    <tr> 
            <th id="T_345ce952_f0f9_11e7_bd73_60f81dc9d130level0_row2" class="row_heading level0 row2" >15 days</th> 
            <td id="T_345ce952_f0f9_11e7_bd73_60f81dc9d130row2_col0" class="data row2 col0" >69</td> 
            <td id="T_345ce952_f0f9_11e7_bd73_60f81dc9d130row2_col1" class="data row2 col1" >87</td> 
        </tr></tbody> 
    </table>

.. |Build Status| image:: https://travis-ci.org/mitmedialab/date_guesser.png?branch=master
   :target: https://travis-ci.org/mitmedialab/date_guesser
.. |Coverage| image:: https://coveralls.io/repos/github/mitmedialab/date_guesser/badge.svg?branch=master
   :target: https://coveralls.io/github/mitmedialab/date_guesser?branch=master
