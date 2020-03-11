import urllib.request

URL = 'https://coronavirus-tracker-api.herokuapp.com/all'
FILENAME = 'covid-19_data.json'

def fetch():
    url = urllib.request.urlopen(urllib.request.Request(URL, headers={
        'User-Agent' : 'https://github.com/coronafighter/coronaSEIR'}))
    r = url.read()
    
    print("read bytes from %s: %i" % (URL, len(r)))
    
    if len(r) < 1000:
        raise Exception("fetch_data.py read less than 1000 bytes")
    
    with open(FILENAME, 'wb') as f:
        f.write(r)
    
if __name__ == '__main__':
    fetch()
