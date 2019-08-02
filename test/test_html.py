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
    test_case = '''
    <html><head>
    <meta property="article:published" content='0'>
    <meta itemprop="datePublished" content='1'>
    <span itemprop="datePublished" datetime='2'></span>
    <meta property="article:published_time" content='3'>
    <meta name="DC.date.published" content='4'>
    <meta name="pubDate" content='5'>
    <time class="buzz-timestamp__time js-timestamp__time" data-unix='6'></time>
    <abbr class="published" title='7'></abbr>
    <span class="timestamp" datetime='8'></span>
    <meta property="nv:date" content='9'>
    <meta itemprop="dateModified" content='10'>
    <meta property="og:updated_time" content='11'>
    <div class="post-meta">12</div>
    <meta name="date_published" content='13'>
    <span class="published">14</span>
    <meta name="citation_date" content='15'>
    <meta name="parsely-pub-date" content='16'>
    <span class="date-display-single" content='17'></span>
    <span name='citation_publication_date' content='18'></span>
    <time datetime='19'></time>
    <meta name="pubdate" content='20'>
    <meta id="absdate" value='21'>
    <meta name="Last-Modified" content='22'>
    <div class="byline">23</div>
    <div class="metadata">24</div>
    <div class="tweet-timestamp" title=25></div>
    <div class='dateline'>26</div>
    <meta property="rnews:datePublished" content='27'>
    <meta name="OriginalPublicationDate" content='28'>
    <meta property="og:published_time" content='29'>
    <meta name="article_date_original" content='30'>
    <meta name="publication_date" content='31'>
    <meta name="sailthru.date" content='32'>
    <meta name="PublishDate" content='33'>
    <meta name="pubdate" datetime='34'>
    <time class="authors__pubdate" datetime='35'>
    </head></html>
    '''
    soup = BeautifulSoup(test_case, 'lxml')
    tag_checkers = get_tag_checkers()
    for idx, tag_checker in enumerate(tag_checkers):
        extracted, method = tag_checker(soup)
        assert extracted == str(idx)
