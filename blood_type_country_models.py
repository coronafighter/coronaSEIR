"""Parse real world country ABH blood type data and solve AB0 SEIR model for every country.

http://www.rhesusnegative.net/themission/bloodtypefrequencies/

Running will show examples of Chile and Pakistan.

todo: change to use wikipedia data?

https://stackoverflow.com/questions/50355577/scraping-wikipedia-tables-with-python-selectively

"""

import matplotlib.pyplot as plt
import matplotlib.widgets  # Cursor
import matplotlib.dates
import numpy as np
from bs4 import BeautifulSoup

import AB0_coronaSEIR


def parse_bt(data):
    s = data.text.replace('20.79.2%', '20.79')
    return float(s.replace('%', '').replace(',', '.'))  # / 100.0


try:
    with open("Blood Type Frequencies by Country including the Rh Factor - Rhesus Negative.html")\
            as f:
        res = f.read()
except FileNotFoundError:  # todo: ask and do it automatically
    raise(Exception("File not found. Save this website to parse: " +
                    "http://www.rhesusnegative.net/themission/bloodtypefrequencies/"))

soup = BeautifulSoup(res, 'lxml')
countryDataPBTD = {}
for items in soup.find('table').find_all('tr')[1::1]:
    data = items.find_all(['th', 'td'])
    country = data[0].text.strip()
    countryDataPBTD[country] = {}
    # Population 	O+ 	A+ 	B+ 	AB+ 	O- 	A- 	B- 	AB-
    countryDataPBTD[country]['population'] = int(data[1].text.replace(',', ''))
    countryDataPBTD[country]['O'] = parse_bt(data[2])
    countryDataPBTD[country]['A'] = parse_bt(data[3])
    countryDataPBTD[country]['B'] = parse_bt(data[4])
    countryDataPBTD[country]['AB'] = parse_bt(data[5])

    countryDataPBTD[country]['O-'] = parse_bt(data[6])
    countryDataPBTD[country]['A-'] = parse_bt(data[7])
    countryDataPBTD[country]['B-'] = parse_bt(data[8])
    countryDataPBTD[country]['AB-'] = parse_bt(data[9])

    if country == 'Zimbabwe':
        break

# fixes
countryDataPBTD['US'] = countryDataPBTD['United States']
countryDataPBTD['South Korea'] = countryDataPBTD['Korea']


def get_bt(country):
    btd = countryDataPBTD[country]
    BT = np.array([btd['A'], btd['B'], btd['AB'], btd['O']])
    return BT / np.sum(BT)

def prepare_and_solve(BT, crossInfectionFactor):
    E0 = BT
    population = 100000
    S0 = BT * population - E0
    return AB0_coronaSEIR.solve_simple(S0, E0, c=crossInfectionFactor)


results = []

def run(crossInfectionFactor=0.5):
    global results, X, I
    for country in countryDataPBTD:
        BT = get_bt(country)
        X, S, E, I, R = prepare_and_solve(BT, crossInfectionFactor)
        countryDataPBTD[country]['I'] = I
        results.append([country, np.max(np.sum(I, axis=0)), BT])
    results = sorted(results, key=lambda x: -x[1])


if __name__ == '__main__':

    run(0.5)

    R = np.array(results)
    maximum = R[:,1].max()
    for r in results:
        print("%35s %.1f" % (r[0], r[1] / maximum * 100.0), r[2])

    fig = plt.figure(dpi=75, figsize=(20, 16))
    ax = fig.add_subplot(211)

    ax.grid(linestyle=':')
    ax.set_xlabel('Time /days')

    cursor = matplotlib.widgets.Cursor(ax, color='black', linewidth=1)

    for country in ['Chile', 'Pakistan']:
        I = countryDataPBTD[country]['I']
        ax.plot(X, np.sum(I, axis=0), alpha=0.6, lw=3, label='Infected %s' % country)
        for i, col in ((3, 'purple'), (1, 'red'), (2, 'blue'), (0, 'orange')):
            ax.plot(X, I[i], color=col, alpha=0.5, lw=1,
                    label='Infected, %s b.t.: %s' % (country, AB0_coronaSEIR.bloodTypes[i]))
    legend = ax.legend(title='COVID-19 SEIR model - blood types distribution (beta)')
