import re

from bs4 import BeautifulSoup

from date_guesser.constants import NO_METHOD
from date_guesser.html import get_tag_checkers, _make_tag_checker


def test__make_tag_checker():
    test_html = '<crazytown strange_class="strange_value" datestring="some_date"></crazytown>'
    tag_checker = _make_tag_checker({'strange_class': 'strange_value'}, attr='datestring')
    soup = BeautifulSoup(test_html, 'lxml')

    extracted, method = tag_checker(soup)
    assert extracted == 'some_date'
    assert 'crazytown' in method

    # Empty html should not extract anything
    assert tag_checker(BeautifulSoup('', 'lxml')) == (None, NO_METHOD)


def test__make_tag_checker_self_closing_tag():
    test_html = '<meta class="foo"/><crazytown class="foo">some_date</crazytown>'
    tag_checker = _make_tag_checker({'class': 'foo'}, text=True)
    soup = BeautifulSoup(test_html, 'lxml')

    extracted, method = tag_checker(soup)
    assert extracted == 'some_date'
    assert 'crazytown' in method


def test_get_tag_checkers():
    test_cases = '''
    <meta property="article:published" content='expected_date_0'>
    <meta itemprop="datePublished" content='expected_date_1'>
    <span itemprop="datePublished" datetime='expected_date_2'></span>
    <meta property="article:published_time" content='expected_date_3'>
    <meta name="DC.date.published" content='expected_date_4'>
    <meta name="pubDate" content='expected_date_5'>
    <time class="buzz-timestamp__time js-timestamp__time" data-unix='expected_date_6'></time>
    <abbr class="published" title='expected_date_7'></abbr>
    <span class="timestamp" datetime='expected_date_8'></span>
    <meta property="nv:date" content='expected_date_9'>
    <meta itemprop="dateModified" content='expected_date_10'>
    <meta property="og:updated_time" content='expected_date_11'>
    <div class="post-meta">expected_date_12</div>
    <meta name="date_published" content='expected_date_13'>
    <span class="published">expected_date_14</span>
    <meta name="citation_date" content='expected_date_15'>
    <meta name="parsely-pub-date" content='expected_date_16'>
    <span class="date-display-single" content='expected_date_17'></span>
    <span name='citation_publication_date' content='expected_date_18'></span>
    <time datetime='expected_date_19'></time>
    <meta name="pubdate" content='expected_date_20'>
    <meta id="absdate" value='expected_date_21'>
    <meta name="Last-Modified" content='expected_date_22'>
    <div class="byline">expected_date_23</div>
    <div class="metadata">expected_date_24</div>
    <div class="tweet-timestamp" title=expected_date_25></div>
    <div class='dateline'>expected_date_26</div>
    <meta property="rnews:datePublished" content='expected_date_27'>
    <meta name="OriginalPublicationDate" content='expected_date_28'>
    <meta property="og:published_time" content='expected_date_29'>
    <meta name="article_date_original" content='expected_date_30'>
    <meta name="publication_date" content='expected_date_31'>
    <meta name="sailthru.date" content='expected_date_32'>
    <meta name="PublishDate" content='expected_date_33'>
    <meta name="pubdate" datetime='expected_date_34'>
    <time class="authors__pubdate" datetime='expected_date_35'>
    '''.split('\n')

    for test_case in test_cases:
        if not test_case.strip():
            continue

        test_case = '<html><head>%s</html></head>' % test_case    

        expected_date = re.search(r'(expected_date_\d+)', test_case).group(1)
        
        soup = BeautifulSoup(test_case, 'lxml')

        for tag_checker in get_tag_checkers():
            extracted, method = tag_checker(soup)
            if extracted:
                assert extracted == expected_date
                break

        assert extracted is not None
