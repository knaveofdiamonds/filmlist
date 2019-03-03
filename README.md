## Find interesting films in London

A small set of scripts that scrapes independent cinema listings, and then
filters them down to:

(a) films in the evening / weekends,
(b) that have a small number of showings over the week

### Usage

First download:

    ./download.sh

Then parse and filter

    python parse.py | python interesting.py

### Setup

1. Have curl and python 3 installed.
2. pip install -r requirements.txt