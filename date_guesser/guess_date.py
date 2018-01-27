import arrow
from bs4 import BeautifulSoup

from .constants import Accuracy, LOCALE, NO_METHOD, Guess
from .dates import MultiDateParser
from .html import get_tag_checkers, get_image_url_checker
from .urls import parse_url_for_date, filter_url_for_undateable


def guess_date(url, html):
    """Guess the date of publication of a webpage.

    Attributes
    ----------
    url : str
        url used to retrieve the webpage
    html : str
        raw html of the webpage

    Returns
    -------
    date_guesser.constants.Guess object.
    """
    return DateGuesser().guess_date(url, html)


class DateGuesser(object):
    def __init__(self):
        self.parser = MultiDateParser(arrow.parser.DateTimeParser(locale=LOCALE))
        self.tag_checkers = get_tag_checkers()
        self.image_url_checker = get_image_url_checker()

    def _choose_better_guess(self, current, new):
        """Logic for deciding if a new guess is better than the previous.

        Attributes
        ----------
        current : date_guesser.constants.Guess object.
            Current datetime and accuracy
        new : date_guesser.constants.Guess object.
            Proposed datetime and accuracy

        Returns
        -------
        date_guesser.constants.Guess object.
            Either current or new
        """
        if current.accuracy >= new.accuracy:
            return current
        elif current.accuracy is Accuracy.NONE:
            return new
        elif current.accuracy is Accuracy.PARTIAL:  # year and month should be right-ish
            if abs((current.date.date() - new.date.date()).days) < 45:
                return new
        elif current.accuracy is Accuracy.DATE:
            if abs((current.date.date() - new.date.date()).days) < 2:
                return new
        return current

    def guess_date(self, url, html):
        """Guess the date of publication of a webpage.

        Attributes
        ----------
        url : str
            url used to retrieve the webpage
        html : str
            raw html of the webpage

        Returns
        -------
        date_guesser.constants.Guess object.
        """
        reason_to_skip = filter_url_for_undateable(url)
        if reason_to_skip is not None:
            return reason_to_skip

        # default guess
        guess = Guess(date=None, accuracy=Accuracy.NONE, method=NO_METHOD)
        # Try using the url
        guess = self._choose_better_guess(guess, parse_url_for_date(url))

        # Try looking for specific elements
        soup = BeautifulSoup(html, 'lxml')
        for tag_checker in self.tag_checkers:
            date_string, method = tag_checker(soup)
            new_date, new_accuracy = self.parser.parse(date_string)
            new_guess = Guess(date=new_date, accuracy=new_accuracy, method=method)
            guess = self._choose_better_guess(guess, new_guess)

        # Try using an image tag
        new_guess = self.guess_date_from_image_tag(soup)
        guess = self._choose_better_guess(guess, new_guess)

        return guess

    def guess_date_from_image_tag(self, soup):
        """Try to use images to extract a url with a date string"""
        image_url, html_method = self.image_url_checker(soup)
        if image_url is not None:
            guess = parse_url_for_date(image_url)
            if guess is not None:
                return Guess(
                    date=guess.date,
                    accuracy=guess.accuracy,
                    method=', '.join([html_method, guess.method]))
        return Guess(date=None, accuracy=Accuracy.NONE, method=NO_METHOD)
