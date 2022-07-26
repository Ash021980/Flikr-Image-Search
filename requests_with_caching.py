import requests
import json
from flicker_creds import api_key
from requests_debugging import requestURL

# Used to cache data retrieved from the api call.
# Ensures that while debugging there aren't excessive api calls.

PERMANENT_CACHE_FNAME = "permanent_cache.txt"
TEMP_CACHE_FNAME = "this_page_cache.txt"
API_KEY = api_key


def _write_to_file(cache, fname):
    with open(fname, 'w') as outfile:
        outfile.write(json.dumps(cache, indent=2))


def _read_from_file(fname):
    try:
        with open(fname, 'r') as infile:
            res = infile.read()
            return json.loads(res)
    except:
        return {}


def add_to_cache(cache_file, cache_key, cache_value):
    temp_cache = _read_from_file(cache_file)
    temp_cache[cache_key] = cache_value
    _write_to_file(temp_cache, cache_file)


def clear_cache(cache_file=TEMP_CACHE_FNAME):
    _write_to_file({}, cache_file)


def make_cache_key(baseurl, params_d, private_keys):
    """Makes a long string representing the query.
    Alphabetize the keys from the params dictionary, so we get the same order each time.
    Omit keys with private info."""

    alphabetized_keys = sorted(params_d.keys())
    res = []

    for k in alphabetized_keys:
        if k not in private_keys:
            res.append("{}-{}".format(k, params_d[k]))
    return baseurl + "_".join(res)


def get(baseurl, params, private_keys_to_ignore=["api_key"], permanent_cache_file=PERMANENT_CACHE_FNAME,
        temp_cache_file=TEMP_CACHE_FNAME):
    """Function that gets the requested api data.  First looks for the data in the temp_cache, then the
       permanent_cache, before using the api call."""

    full_url = requestURL(baseurl, params)
    cache_key = make_cache_key(baseurl, params, private_keys_to_ignore)

    # Load the permanent and page-specific caches from files
    permanent_cache = _read_from_file(permanent_cache_file)
    temp_cache = _read_from_file(temp_cache_file)

    if cache_key in temp_cache:
        print("found in temp_cache")
        # make a Response object containing text from the change, and the full_url that would have been fetched
        return json.loads(temp_cache[cache_key])
    elif cache_key in permanent_cache:
        print("found in permanent_cache")
        # make a Response object containing text from the change, and the full_url that would have been fetched
        return json.loads(permanent_cache[cache_key])
    else:
        print("new; adding to cache")
        # actually request it
        resp = requests.get(baseurl, params)
        # save it
        add_to_cache(temp_cache_file, cache_key, resp.text)
        return resp
