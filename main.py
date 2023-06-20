#!/usr/bin/env python3.11

import argparse
import bs4
import logging
import os
import requests
import sys
import urllib.parse

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
    parser.add_argument('--download_location', type=str, required=False, default='downloads')
    parser.add_argument('--filter_extension', type=str, required=False, default='.mp3')
    parser.add_argument('--delay', type=int, required=False, default=5)
    parser.add_argument('--retries', type=int, required=False, default=5)
    parser.add_argument('--retry_delay', type=int, required=False, default=30)

    log.debug("Argument parser set up!")

    args = parser.parse_args()

    log.debug(f"Arguments parsed: {args}")

    log.info("Requesting page...")
    page = requests.get(args.url).text
    soup = bs4.BeautifulSoup(page, 'html.parser')
    log.debug("Page requested and parsed.")

    log.info(f"Pulling links for '{args.filter_extension}' files...")
    links = [node.get('href') for node in soup.body.find_all('a') if node.get('href').endswith(args.filter_extension)]
    log.debug(f"'{args.filter_extension}'s found on page: {len(links)}")

    log.debug("Does our download directory exist?")
    if not os.path.exists(args.download_location):
        log.debug("It does not. Creating that now.")
        try:
            os.mkdir(args.download_location)
        except Exception as err:
            log.fatal("Unable to create download directory. Good bye")
            exit()
    else:
        log.debug("It does! Continuing")

    log.debug("Final checks on URL: Does it end in a '/'?")
    if not args.url.endswith('/'):
        log.debug("It does not. Adding that now.")
        args.url = args.url + '/'
    else:
        log.debug("Check passed. Continuing")


    for link in links:
        for attempt in range(args.retries):
            unlink = urllib.parse.unquote(link)

            break
        

    

if __name__ == '__main__':
    main()