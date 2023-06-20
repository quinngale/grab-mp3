#!/usr/bin/env python3.11

import argparse
import bs4
import logging
import os
import requests
import sys
import time
import urllib.parse

APP_NAME = sys.argv[0]
APP_DESC = "A utility to grab MP3 files from the provided URL"

def main() -> None:
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
    parser.add_argument('--exit_on_error', type=bool, required=False, default=False)

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
        log.debug("It dows! Continuing")


    for link in links:
        unlink = urllib.parse.unquote(link)
        log.debug(f"File to download: {unlink}")
        newfilename = os.path.join(args.download_location, unlink)

        log.debug(f"Testing to see if \"{unlink}\" exists...")
        if os.path.exists(newfilename):
            log.info(f"{newfilename} exists already, so we are skipping the download.")
            continue

        for attempt in range(args.retries):
            log.debug(f"Starting attempt {attempt + 1} of {args.retries}:")

            try:
                log.debug(f"But first, let me take a quick nap ({args.delay} seconds)...")
                time.sleep(args.delay)
                
                log.info(f"Downloading \"{unlink}\" from \"{args.url}\"...")
                request = requests.get(f"{args.url}{link}")

                try:
                    log.debug("Trying to write the contents to the disk...")
                    with open(newfilename, 'wb') as newfile:
                        newfile.write(request.content)

                except Exception:
                    log.error("We were unable to open \"{newfilename}\" for writing.")
                    if args.exit_on_error:
                        log.fatal("Exiting")
                        exit()

                break

            except Exception:
                if attempt == args.retries - 1:
                    log.error(f"We were unable to download {unlink} in {attempt + 1} tries")
                    if args.exit_on_error:
                        log.fatal("Good bye.")

                else:
                    log.warning(f"There was an error. Retrying again in {args.retry_delay} seconds ({attempt + 1} of {args.retries})")
                    time.sleep(args.retry_delay - args.delay)


if __name__ == '__main__':
    main()