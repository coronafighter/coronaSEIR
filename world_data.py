import json
import dateutil.parser
import datetime
import os.path
import time

import scipy.ndimage.interpolation  # shift function
def delay(npArray, days):
    return scipy.ndimage.interpolation.shift(npArray, days, cval=0)

import fetch_data

FILENAME = fetch_data.FILENAME
CACHETIMESECONDS = 3600 * 3  # be nice to the API to not get banned

if (not os.path.exists(FILENAME) or 
    os.path.getmtime(FILENAME) < time.time() - CACHETIMESECONDS):
        fetch_data.fetch()

with open(FILENAME) as f:
    s = f.read()
    s = s.replace('Iran (Islamic Republic of)', 'Iran')  # obsolete?
    s = s.replace('Mainland China', 'China')  # obsolete ?
    print("read data: %i bytes" % len(s))
d = json.loads(s)

def get_country_xcdr(country='all', province='all', excludeCountries=[], excludeProvinces=[],
                     dateOffset=0, returnLists=False, returnDates=False):
    country = '' if country == 'all' else country  # empty string is same as all
    province = '' if province == 'all' else province
    countries = {}
    provinces = {}

    dictXYYY = {}
    XDatesAll = []

    for i, location in enumerate(d['confirmed']['locations']):
        XDates = []
        YConfirmed = []
        YDeaths = []
        YRecovered = []
        listXYYY = []

        countries[str(location['country'])] = 1
        if country != '' and location['country'] != country:
            continue
        if location['country'] in excludeCountries:
            print("Excluded country:", location['country'])
            continue
        provinces[str(location['province'])] = 1
        if province != '' and location['province'] != province:
            continue
        if location['province'] in excludeProvinces:  # global provinces can't have the same name
            print("Excluded province:", province)
            continue
        for date in location['history']:
            confirmed = int(location['history'][date])
            deaths = int(d['deaths']['locations'][i]['history'][date])
            try:
                recovered = int(d['recovered']['locations'][i]['history'][date])
            except (KeyError, IndexError):
                recovered = 0
            XDates.append(dateutil.parser.parse(date))
            YConfirmed.append(confirmed)
            YDeaths.append(deaths)
            YRecovered.append(recovered)

        for i, date in enumerate(XDates):
            if date in dictXYYY:
                dictXYYY[date][0] += YConfirmed[i]
                dictXYYY[date][1] += YDeaths[i]
                dictXYYY[date][2] += YRecovered[i]
            else:    
                dictXYYY[date] = [YConfirmed[i], YDeaths[i], YRecovered[i]]
        XDatesAll.extend(XDates)
    
    listXYYY = []
    XDatesAllNonEmpty = []
    for date in dictXYYY:
        day = (date - min(XDatesAll)).days + dateOffset
        C, D, R = dictXYYY[date][0], dictXYYY[date][1], dictXYYY[date][2]
        if (C + D + R) > 0:
            if returnDates:
                x = date
            else:
                x = day
            listXYYY.append((x, C, D, R))
            XDatesAllNonEmpty.append(date)
    listXYYY.sort()  # in place by first item
    
    # parse countries just to display available ones in case of error
    if returnLists:
        countries = list(countries.keys())
        countries.sort()
        provinces = list(provinces.keys())
        provinces.sort()
        return countries, provinces

    if len(listXYYY) == 0:
        countries, provinces = get_countries_provinces()
        if not country in countries:
            print(countries)
        if not province in provinces:
            print()
            print(provinces)
        raise Exception("get_country_xcdr empty - country '%s' or province '%s' not found?" % (country, province))

    print("todays date: %s" % datetime.date.today())
    print("data points for %s: %s" % (country, len(listXYYY)))
    print("first data: %s" % min(XDatesAllNonEmpty).date())
    print("latest data: %s (you can update the data manually by running fetch_data.py)" % max(XDatesAll).date())

    return listXYYY

def get_countries_provinces():
    countries, provinces = get_country_xcdr(returnLists=True)
    return countries, provinces

if __name__ == '__main__':
    import numpy as np
    import matplotlib.pyplot as plt

    fig = plt.figure(figsize=(10,10), dpi=200)
    ax = fig.add_subplot(211)

    COUNTRY = 'Italy'
    PROVINCE = 'all'
    XYYY = np.array(get_country_xcdr(COUNTRY, PROVINCE))
    X = XYYY[:,0]

    #ax.set_yscale("log", nonposy='clip')
    ax.plot(X, XYYY[:,1], 'b', alpha=0.5, lw=2, label='confirmed')
    ax.plot(X, XYYY[:,2], 'y', alpha=0.5, lw=2, label='deaths')
    ax.plot(X, XYYY[:,3], 'r--', alpha=0.5, lw=1, label='recovered')
    ax.legend(title='COVID-19 data (beta): ' + COUNTRY + " " + PROVINCE)

    ax2 = fig.add_subplot(212)

    COUNTRY = 'all'
    excludeCountries = ['China']
    PROVINCE = 'all'

    XYYY = np.array(get_country_xcdr(COUNTRY, PROVINCE, excludeCountries=excludeCountries))
    X = XYYY[:,0]

    #ax2.set_yscale("log", nonposy='clip')
    ax2.plot(X, XYYY[:,1], 'b', alpha=0.5, lw=2, label='confirmed')
    ax2.plot(X, XYYY[:,2], 'y', alpha=0.5, lw=2, label='deaths')
    ax2.plot(X, XYYY[:,3], 'r--', alpha=0.5, lw=1, label='recovered')
    ax2.legend(title='COVID-19 data (beta): all but China')
    plt.show()
    #plt.savefig('data.png')

