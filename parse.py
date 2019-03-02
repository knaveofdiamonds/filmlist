import sys

from bs4 import BeautifulSoup


def extract_cinema(html):
    return html.title.text.replace(
        ' Cinema - London - Listings and Film Reviews',
        ''
    )


def extract_raw_showings(html):
    nodes = html.select('#cin_starting_thisweek .venuefilmbloc')

    return [
        {'title': n.find('a').text, 'times': n.find('span').text}
        for n in nodes
    ]


if __name__ == '__main__':
    html = BeautifulSoup(sys.stdin.read(), 'lxml')
