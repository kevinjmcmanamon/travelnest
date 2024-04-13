# Travelnest Scraper

## Overview
This repository hosts a web scraper designed to extract property attributes from
various URLs.

The tests contained within `tests/integration/test_airbnb_scraper.py` contains a
working example of the specified behaviour (i.e. fetching property attributes
from 3 AirBnB pages).

## Features
- Fetches data from URLs
- Parses HTML content to extract property attributes
- Handles parsing and fetching errors gracefully
- Implemented so that new types of parsers for different sites should be easy to plug in

## Future work
- If the number of URLs were to grow significantly, you could look to de-couple
the fetching from the parsing, which is currently done sequentially.
    - This is one reason why I've separated the fetching from the parsing, in
    order to make these kind of future refactorings easier.
- Could use multi-threading to fetch many URLs in parallel.  Then perhaps use
some sort of queuing system to feed that data into a parsing / processing
module.
- The code that actually parses the HTML could perhaps be improved.
Fortunately, any refactoring of that component will not affect any other parts
of the code.
- Currently the parser just returns a plain dictionary.  This could perhaps be updated to use a more formal data stucture, such as a dataclass.