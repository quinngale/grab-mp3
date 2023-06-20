# MP3 Grabber

A short python file to grab linked MP3 files from a provided URL.

## Installing dependencies

This Python script has two dependencies: BeautifulSoup and requests. To install them run the following command:

```sh
pip install -f requirements.txt
```

## Running the program

This program has one required argument and a bunch of optional arguments to modify its behavior. The only required argument is `url`. This tells the program where to go to download the files. Example:

```sh
python main.py https://lab.quinngale.com/
```

### Optional arguments

-   `--download_location`: Where to download the files to. Default is `downloads`
-   `--filter_extension`: The file type you want to grab. Default is `.mp3`
-   `--delay`: How long to wait between each download in seconds. Default is `5`
-   `--retries`: How many retries to make if a download fails. Default is `5`
-   `--retry_delay`: How many seconds to wait before attempt again if a download fails in seconds. Default is `30`
-   `--exit_on_error`: If this is `True`, the program will exit if there is an error. Default is `False`
