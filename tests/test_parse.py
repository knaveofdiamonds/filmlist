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


def test_parse_showings_single_day_time():
    assert subject.parse_showings('Mon 20:45') == [
        {'day': 'Mon', 'time': '20:45'},
    ]


def test_parse_showings_single_day_multiple_times():
    assert subject.parse_showings('Mon 15:30 20:45') == [
        {'day': 'Mon', 'time': '20:45'},
        {'day': 'Mon', 'time': '15:30'},
    ]


def test_parse_showings_multiple_day_multiple_times():
    assert subject.parse_showings('Mon/Wed 15:30 20:45') == [
        {'day': 'Wed', 'time': '20:45'},
        {'day': 'Wed', 'time': '15:30'},
        {'day': 'Mon', 'time': '20:45'},
        {'day': 'Mon', 'time': '15:30'},
    ]


def test_parse_showings_separate_showings():
    assert subject.parse_showings('Mon 15:30; Tue 20:45') == [
        {'day': 'Tue', 'time': '20:45'},
        {'day': 'Mon', 'time': '15:30'},
    ]


def test_expand_day_range():
    assert subject.expand_day_range("Mon", "Wed") == ["Mon", "Tue", "Wed"]
    assert subject.expand_day_range("Fri", "Wed") == [
        "Fri", "Sat", "Sun",
        "Mon", "Tue", "Wed"
    ]
    assert subject.expand_day_range("Fri", "Sat") == ["Fri", "Sat"]


def test_parse_showings_day_range():
    assert subject.parse_showings('Mon-Wed 20:45') == [
        {'day': 'Mon', 'time': '20:45'},
        {'day': 'Tue', 'time': '20:45'},
        {'day': 'Wed', 'time': '20:45'},
    ]


def test_parse_showings_day_range_qualified_time():
    result = subject.parse_showings('Mon-Wed 15:30 (Tue) 20:45')

    assert len(result) == 4
    assert result == [
        {'day': 'Mon', 'time': '20:45'},
        {'day': 'Tue', 'time': '20:45'},
        {'day': 'Tue', 'time': '15:30'},
        {'day': 'Wed', 'time': '20:45'},
    ]


def test_parse_showings_no_day_expression():
    assert subject.parse_showings('20:45') == [
        {'day': 'Mon', 'time': '20:45'},
        {'day': 'Tue', 'time': '20:45'},
        {'day': 'Wed', 'time': '20:45'},
        {'day': 'Thu', 'time': '20:45'},
        {'day': 'Fri', 'time': '20:45'},
        {'day': 'Sat', 'time': '20:45'},
        {'day': 'Sun', 'time': '20:45'},
    ]
