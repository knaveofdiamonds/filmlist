import os

from bs4 import BeautifulSoup
import pytest

import parse as subject


@pytest.fixture
def html():
    test_file = os.path.join(
        os.path.dirname(__file__),
        'test.html'
    )

    with open(test_file, 'r') as fh:
        raw = fh.read()

    return BeautifulSoup(raw, 'lxml')


def test_cinema(html):
    assert subject.extract_cinema(html) == 'Clapham Picturehouse'


def test_extract_raw_showings(html):
    raw_showings = subject.extract_raw_showings(html)

    assert len(raw_showings) == 17
    assert raw_showings[0]['title'] == 'Alien'
    assert raw_showings[0]['times'] == 'Mon 20:45'
