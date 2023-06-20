#!/usr/bin/env python3.11

import argparse
import logging
import sys
import xml

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

    parser = argparse.ArgumentParser(prog=APP_NAME, description=APP_DESC)
    parser.add_argument('url', type=str)

    args = parser.parse_args()

    url = args.url

if __name__ == '__main__':
    main()