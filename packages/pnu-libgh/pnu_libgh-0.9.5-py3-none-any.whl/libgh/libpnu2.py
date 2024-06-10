#!/usr/bin/env python3
""" libgh - GitHub scraping library and tool
License: 3-clause BSD (see https://opensource.org/licenses/BSD-3-Clause)
Author: Hubert Tournier
"""

import datetime
import hashlib
import logging
import lzma
import os
import re
import time
import urllib.request

import libpnu

HTTP_HEADERS = {
    "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
    "Accept": "*/*",
    "Accept-Language": "en;q=1.0, *;q=0.5",
    "Accept-Encoding": "identity",
    "Connection": "close",
}


####################################################################################################
def _count_from(current_time, requests_times):
    """ Returns the number of requests made in the last day, hour and minute """
    last_day = 0
    last_hour = 0
    last_minute = 0

    one_day = 24 * 60 * 60 # seconds
    one_hour = 60 * 60 # seconds
    one_minute = 60 # seconds

    # The requests_times is not necessarily ordered by ascending timestamps...
    for request_time in requests_times:
        time_diff = current_time - request_time
        if time_diff <= one_day:
            last_day += 1
        if time_diff <= one_hour:
            last_hour += 1
        if time_diff <= one_minute:
            last_minute += 1

    return last_day, last_hour, last_minute

####################################################################################################
def get_url_bdata(
    url,
    cache_dir,
    headers={},
    cache_days=1,
    cache_index=False,
    force_fetch=False,
    min_delay=0,
    max_per_minute=-1,
    max_per_hour=-1,
    max_per_day=-1,
    timeout=15
):
    """ Returns an URL binary data and HTTP headers from a recent cache file or from the Web """
    current_time = time.time()
    directory = libpnu.get_caching_directory(cache_dir)

    # Keep a persistent history of URL fetched from the Web
    if not hasattr(get_url_bdata, "history"):
        get_url_bdata.history = {}

        # Load relevant history from the index file if it exist
        index_name = f"{directory}{os.sep}index.txt"
        lines = []
        if os.path.isfile(index_name):
            with open(index_name, encoding="utf-8", errors="ignore") as file:
                lines = file.read().splitlines()
        for line in lines:
            fields = line.split("#")
            date = datetime.datetime.strptime(fields[2], "%Y-%m-%d %H:%M:%S.%f")
            timestamp = datetime.datetime.timestamp(date)
            if current_time - timestamp <= cache_days * 24 * 60 * 60:
                website = re.sub(r"https*://", "", fields[0])
                website = re.sub(r"/.*", "", website)
                if website in get_url_bdata.history:
                    get_url_bdata.history[website].append(timestamp)
                else:
                    get_url_bdata.history[website] = [timestamp]

    # If there's a fragment reference in the URL, remove it
    # (else we would risk storing several time the same file)
    if '#' in url:
        url = re.sub(r"#.*", "", url)
    if "%23" in url:
        url = re.sub(r"%23.*", "", url)

    # Create an obfuscated and sanitized cache file name from the URL
    # (both to avoid any special characters in filenames and to offer
    # some privacy about what's in the cache, unless an index file is
    # used of course)
    digest = hashlib.sha256()
    digest.update(str.encode(url, encoding="utf-8", errors="ignore"))
    cache_file = digest.hexdigest() + ".xz"

    # Add 2 levels of sub directories to avoid using a flat storage space
    # (for 65K maximum sub directories)
    cache_file = re.sub(r"^(..)(..)(.*)", f"\g<1>{os.sep}\g<2>{os.sep}\g<3>", cache_file)

    # Make it a full pathname
    if directory:
        filename = directory + os.sep + cache_file
    else:
        filename = cache_file

    # Create directories if needed
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    # Use a cache file if cache_days != 0
    if not force_fetch and cache_days:
        # If there's a cache file of less than cache_days, return its data
        if os.path.isfile(filename) \
        and (current_time - os.path.getmtime(filename)) < cache_days * 24 * 60 * 60:
            logging.debug("libpnu/get_url_bdata: Loading '%s' from cache", url)
            with lzma.open(filename) as file:
                bdata = file.read()
            return bdata, []

    # Else fetch the URL contents from the Web

    # Shall we wait before fetching the URL?
    current_date = datetime.datetime.fromtimestamp(current_time)
    website = re.sub(r"https*://", "", url)
    website = re.sub(r"/.*", "", website)
    if website in get_url_bdata.history:
        last_day, last_hour, last_minute = _count_from(current_time, get_url_bdata.history[website])
        logging.debug(
            "libpnu/get_url_bdata: Web requests to '%s' last day=%d, hour=%d, min=%d",
            website,
            last_day,
            last_hour,
            last_minute
        )
        slowing_down = False
        if last_day >= max_per_day > 0:
            logging.debug("libpnu/get_url_bdata: Max requests per day reached. Sleeping for 1 day")
            time.sleep(24 * 60 * 60)
            slowing_down = True
        if last_hour >= max_per_hour > 0:
            logging.debug(
                "libpnu/get_url_bdata: Max requests per hour reached. Sleeping for 1 hour"
            )
            time.sleep(60 * 60)
            slowing_down = True
        if last_minute >= max_per_minute > 0:
            logging.debug(
                "libpnu/get_url_bdata: Max requests per minute reached. Sleeping for 1 minute"
            )
            time.sleep(60)
            slowing_down = True
        if slowing_down:
            current_time = time.time()
            current_date = datetime.datetime.fromtimestamp(current_time)

        if min_delay:
            time_diff = current_time - get_url_bdata.history[website][-1]
            if time_diff < min_delay:
                time_wait = min_delay - time_diff
                logging.debug(
                    "libpnu/get_url_bdata: Slowing down URL fetching. Sleeping for %f seconds",
                    time_diff
                )
                time.sleep(time_wait)
                current_time = time.time()
                current_date = datetime.datetime.fromtimestamp(current_time)

        get_url_bdata.history[website].append(current_time)
    else:
        get_url_bdata.history[website] = [current_time]

    # Let's go now!
    logging.debug("libpnu/get_url_bdata: Loading '%s' from the Web", url)
    all_headers = HTTP_HEADERS
    for key, value in headers.items():
        all_headers[key] = value
    request = urllib.request.Request(url, headers=all_headers)
    response = []
    try:
        with urllib.request.urlopen(request, timeout=timeout) as http:
            bdata = http.read()
        response = http.getheaders()
    except urllib.error.HTTPError as error:
        if error == 'HTTP Error 429: Too Many Requests':
            raise PermissionError(f"Max requests reached for '{website}'") from error

        if error == 'HTTP Error 404: Not Found':
            # Write an empty file to avoid retrying later...
            with lzma.open(filename, "wb") as file:
                pass

        raise LookupError(f"Error while fetching '{url}': {error}") from error

    # Cache the URL contents for future requests
    with lzma.open(filename, "wb") as file:
        file.write(bdata)

    # If requested, write the correspondance between the url and the obfuscated cache file name
    if cache_index:
        if directory:
            index_filename = f"{directory}{os.sep}index.txt"
        else:
            index_filename = "index.txt"
        with open(index_filename, "at", encoding="utf-8", errors="ignore") as file:
            file.write(f"{url}#{cache_file}#{current_date}\n")

    return bdata, response

####################################################################################################
def get_url_data(
    url,
    cache_dir,
    headers={},
    cache_days=1,
    cache_index=False,
    force_fetch=False,
    min_delay=0,
    max_per_minute=-1,
    max_per_hour=-1,
    max_per_day=-1,
    timeout=15
):
    """ Returns an URL text data and HTTP headers from a recent cache file or from the Web """
    bdata, response = get_url_bdata(
        url,
        cache_dir,
        headers=headers,
        cache_days=cache_days,
        cache_index=cache_index,
        force_fetch=force_fetch,
        min_delay=min_delay,
        max_per_minute=max_per_minute,
        max_per_hour=max_per_hour,
        max_per_day=max_per_day,
        timeout=timeout
    )

    return bdata.decode("utf-8", "ignore"), response

####################################################################################################
def prune_cache(cache_dir, cache_days):
    """ Removes old files and their index entries, and unused directories from the cache dir """
    directory = libpnu.get_caching_directory(cache_dir)
    if not directory:
        # Don't take the risk to remove files
        return

    # Load the index file if it exist
    index_name = f"{directory}{os.sep}index.txt"
    lines = []
    if os.path.isfile(index_name):
        with open(index_name, encoding="utf-8", errors="ignore") as file:
            lines = file.read().splitlines()

    # Remove duplicates
    index = {}
    for line in lines:
        fields = line.split("#")
        url = fields[0]
        filename = fields[1]
        timestamp = fields[2]
        index[filename] = {"url": url, "timestamp": timestamp}

    # Remove old files and their index entries
    current_time = time.time()
    for root, _, files in os.walk(directory):
        for file in files:
            if file != "index.txt":
                pathname = root + os.sep + file
                filename = re.sub(f"^{directory}{os.sep}", "", pathname)
                if current_time - os.path.getmtime(pathname) > cache_days * 24 * 60 * 60:
                    os.remove(pathname)
                    if filename in index:
                        del index[filename]

    # Recreate the index file if needed
    if index:
        with open(index_name, "w", encoding="utf-8", errors="ignore") as file:
            for cache_file, value in index.items():
                url = value["url"]
                timestamp = value["timestamp"]
                file.write(f"{url}#{cache_file}#{timestamp}\n")

    # Remove empty directories
    subdirs = list(os.walk(directory, topdown=False))
    for subdir in subdirs:
        try:
            os.rmdir(subdir[0])
        except OSError:
            # subdir is not empty
            pass

####################################################################################################
def collection2xml(data, name="root", depth=0, indent_size=2, show_types=False):
    """ Returns the collection data type as a list of XML lines """
    xml = []
    data_type = str(type(data))[8:-2]

    if depth == 0:
        xml.append('<?xml version="1.0" encoding="UTF-8" ?>')
        xml.append(f"<{name}>")
        xml += collection2xml(
            data,
            depth=1,
            indent_size=indent_size,
            show_types=show_types
        )
        xml.append(f"</{name}>")
    elif data_type == "dict":
        for key, value in data.items():
            if key.lower().startswith("xml") \
            or not key[0].isalpha() and key[0] != '_':
                key = f"_{key}"
            key = key.replace(" ", "_")
            key = key.replace("/", "&sol;")
            value_type = str(type(value))[8:-2]
            strtype = ""
            if show_types:
                strtype = f' type="{value_type}"'
            if value_type == "dict":
                xml.append(f"{depth * indent_size * ' '}<{key}{strtype}>")
                xml += collection2xml(
                    value,
                    depth=depth + 1,
                    indent_size=indent_size,
                    show_types=show_types
                )
                xml.append(f"{depth * indent_size * ' '}</{key}>")
            elif value_type == "list":
                xml.append(f"{depth * indent_size * ' '}<{key}{strtype}>")
                xml += collection2xml(
                    value,
                    name=key,
                    depth=depth + 1,
                    indent_size=indent_size,
                    show_types=show_types
                )
                xml.append(f"{depth * indent_size * ' '}</{key}>")
            elif value_type in ("bool", "int", "float", "complex"):
                xml.append(f"{depth * indent_size * ' '}<{key}{strtype}>{value}</{key}>")
            elif value_type == "str":
                value = value.replace("&","&amp;")
                value = value.replace(">","&gt;")
                value = value.replace("<","&lt;")
                xml.append(f"{depth * indent_size * ' '}<{key}{strtype}>{value}</{key}>")
            else:
                logging.error("libpnu/collection2xml: value type '%s' not processed. Skipping it")
    elif data_type in ("tuple", "list", "set", "frozenset"):
        for value in data:
            value_type = str(type(value))[8:-2]
            strtype = ""
            if show_types:
                strtype = f' type="{value_type}"'
            if value_type == "dict":
                xml.append(f"{depth * indent_size * ' '}<{name}_item{strtype}>")
                xml += collection2xml(
                    value,
                    depth=depth + 1,
                    indent_size=indent_size,
                    show_types=show_types
                )
                xml.append(f"{depth * indent_size * ' '}</{name}_item>")
            elif value_type == "list":
                xml.append(f"{depth * indent_size * ' '}<{name}_item{strtype}>")
                xml += collection2xml(
                    value,
                    depth=depth + 1,
                    indent_size=indent_size,
                    show_types=show_types
                )
                xml.append(f"{depth * indent_size * ' '}</{name}_item>")
            elif value_type in ("bool", "int", "float", "complex"):
                xml.append(
                    f"{depth * indent_size * ' '}<{name}_item{strtype}>{value}</{name}_item>"
                )
            elif value_type == "str":
                value = value.replace("&","&amp;")
                value = value.replace(">","&gt;")
                value = value.replace("<","&lt;")
                xml.append(
                    f"{depth * indent_size * ' '}<{name}_item{strtype}>{value}</{name}_item>"
                )
            else:
                logging.error("libpnu/collection2xml: value type '%s' not processed. Skipping it")

    return xml
