#!/usr/bin/env python3.11

import argparse
import bs4
import logging
import requests
import sys


APP_NAME = sys.argv[0]
APP_DESC = "A utility to grab MP3 files from the provided URL"

def main():
    log = logging.getLogger(APP_NAME)
    if hasattr(sys, 'gettrace') and sys.gettrace() is not None:
        log.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.INFO)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

    consoleHandler.setFormatter(formatter)

    log.addHandler(consoleHandler)

    log.debug("Logging set up!")

    parser = argparse.ArgumentParser(prog=APP_NAME, description=APP_DESC)
    parser.add_argument('url', type=str)

    log.debug("Argument parser set up!")

    args = parser.parse_args()

    log.debug(f"Arguments parsed: {args}")

    url = args.url

    log.info("Requesting page...")
    page = requests.get(url).text
    soup = bs4.BeautifulSoup(page, 'html.parser')
    log.info("Page requested and parsed.")

    links = [node.get('href') for node in soup.body.find_all('a') if node.get('href').endswith('.mp3')]
    log.debug(f"MP3s found on page: {len(links)}")
    

if __name__ == '__main__':
    main()