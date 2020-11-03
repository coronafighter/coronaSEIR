import time
import os
import urllib.request

import shared


def fetch(url=shared.APIURL):
    url = urllib.request.urlopen(urllib.request.Request(url, headers={
        'User-Agent': 'https://github.com/coronafighter/coronaSEIR'}))
    r = url.read()

    print("read bytes from %s: %i" % (shared.APIURL, len(r)))

    if len(r) < 1000:
        raise Exception("fetch_data.py read less than 1000 bytes")

    with open(shared.FILENAME, 'wb') as f:
        f.write(r)


def handle_fetch():
    if (not os.path.exists(shared.FILENAME) or
            os.path.getmtime(shared.FILENAME) < time.time() - shared.CACHETIMESECONDS):
        try:
            fetch(shared.APIURL)
        except urllib.request.HTTPError:
            print("could not reach API server - trying fallback server")
            try:
                fetch(shared.APIURLFALLBACK)
            except Exception:
                print("could not reach fallback API server either - trying (outdated) local file - press <enter>")
                input()


if __name__ == '__main__':
    handle_fetch()
