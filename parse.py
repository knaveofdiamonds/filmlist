import itertools
import sys

from bs4 import BeautifulSoup
from parsimonious.grammar import Grammar
from parsimonious.nodes import NodeVisitor


SHOWINGS_GRAMMAR = Grammar(
"""
showings = showing (";" whitespace showing)*
showing  = day_expression? (whitespace? time_expression)+
day_expression = day_or_day_range ("/" day_or_day_range)*
day_or_day_range = day ("-" day)?
day  = ~"Mon|Tue|Wed|Thu|Fri|Sat|Sun"
time_expression = time (whitespace time_qualifier)?
time_qualifier = "(" day ")"
time = ~"[0-2]?[0-9]:[0-5][0-9]"
whitespace = ~"\s+"
"""
)

DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

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


def expand_day_range(start_day, end_day):
    i = DAYS.index(start_day)
    j = DAYS.index(end_day)

    if i < j:
        return DAYS[i:j+1]
    else:
        return DAYS[i:len(DAYS)] + DAYS[0:j+1]


def parse_showings(time_str):
    ast = SHOWINGS_GRAMMAR.parse(time_str)

    result = []
    node_stack = [ast]

    # context variables
    times = []
    days = []
    time_qualifier = None
    in_showing = False

    while len(node_stack) != 0:
        n = node_stack.pop()

        if n.expr_name == 'time':
            if time_qualifier:
                times.append((n.text, time_qualifier))
                time_qualifier = None
            else:
                times.append((n.text, None))
        elif n.expr_name == 'time_qualifier':
            time_qualifier = n.children[1].text
        elif n.expr_name == 'day_or_day_range':
            if '-' in n.text:
                days += expand_day_range(*(n.text.split('-')))
            else:
                days.append(n.text)
        elif n.expr_name == 'showing':
            if in_showing:
                in_showing = False

                if not days:
                    days = DAYS

                result += [
                    {'day': day, 'time': time[0]}
                    for (day, time) in itertools.product(days, times)
                    if time[1] is None or time[1] == day
                ]
            else:
                times = []
                days = []
                in_showing = True

                # Push the showing node back onto the stack so we process all
                # the child day / time nodes before collecting into results
                node_stack.append(n)

                for child in n:
                    node_stack.append(child)
        else:
            for child in n:
                node_stack.append(child)

    return result


if __name__ == '__main__':
    html = BeautifulSoup(sys.stdin.read(), 'lxml')
    showings = extract_raw_showings(html)

    for s in showings:
        times = parse_showings(s['times'])

        print(f"## {s['title']} ##")

        for t in times:
            print(t)
