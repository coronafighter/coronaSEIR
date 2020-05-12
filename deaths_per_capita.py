import sys
import numpy as np
import matplotlib.pyplot as plt

import population
import world_data

countries, provinces = world_data.get_countries_provinces()
countryPopulation = population.get_all_population_data()
countries.extend(['Hubei'])

# todo: single loop, cleanup

countryDeaths = []
for country in countries:
    try:
        if countryPopulation[country] < 1000000:
            continue
        province = 'all'
        country2 = country
        if country == 'Hubei':
            country2 = 'China'
            province = 'Hubei'
        XCDR_data = np.array(world_data.get_country_xcdr(country2, province=province,
                                                         returnDates=True))
        cases = int(XCDR_data[-1, 1])  # last row, third column
        deaths = int(XCDR_data[-1, 2])  # last row, third column
        deathDelta = int(XCDR_data[-1, 2] - XCDR_data[-8, 2])
        if deaths < 10:
            continue
        recovered = int(XCDR_data[-1, 3])  # last row, third column
        date = XCDR_data[-1, 0]
        countryDeaths.append((country, cases, deaths, recovered, date, deathDelta))

    except Exception as e:
        print("fail: ", country, sys.exc_info()[0], e)

countryDeathsPC = []
countryDeathsDeltaPC = []
for ccdrd in countryDeaths:
    country, cases, deaths, recovered, date, deathDelta = ccdrd
    try:
        pop = population.get_population(country)
        countryDeathsPC.append((country, deaths * 1.0e6 / pop, deaths, pop, date))
        countryDeathsDeltaPC.append((country, deathDelta * 1.0e6 / pop, deathDelta, pop, date))
        #countryDeathrate.append((country, 100.0 * deaths / cases, deaths, pop))
    except KeyError:
        print("fail: ", country)

print()
countryDeathsPC = sorted(countryDeathsPC, key = lambda x: x[1])  # sort by second subitem
countryDeathsPC.reverse()  # in place

countryDeathsDeltaPC = sorted(countryDeathsDeltaPC, key = lambda x: x[1])  # sort by second subitem
countryDeathsDeltaPC.reverse()  # in place


dCountryDeathsPCXY = {}
for country, trash, trash, trash, trash in countryDeathsPC[0:20]:
    province = 'all'
    country2 = country
    if country == 'Hubei':
        country2 = 'China'
        province = 'Hubei'
    XCDR_data = np.array(world_data.get_country_xcdr(country2, province=province, returnDates=True))
    pop = population.get_population(country)
    #Y = 100.0 * XCDR_data[:,2] / XCDR_data[:,1] 
    Y = XCDR_data[:,2] / pop * 1.0e6
    dCountryDeathsPCXY[country] = (XCDR_data[:,0], Y)

fig = plt.figure(dpi=75, figsize=(20,16))
ax = fig.add_subplot(111)
#ax.set_yscale("log", nonposy='clip')

for country in dCountryDeathsPCXY:
    ax.plot(dCountryDeathsPCXY[country][0], dCountryDeathsPCXY[country][1],
            alpha=0.5, lw=2, label=country)

legend = ax.legend(title='deaths per 1M capita (beta)')

print()
print('beta, there might be bugs')
print('current deaths per capita')
for country, deathsPC, deaths, pop, date in countryDeathsPC[0:20]:
    print("%-15s" % country, ': %10.1f %5d %10d %s' % (deathsPC, deaths, pop, date.strftime("%Y-%m-%d")))

print()
print('new deaths per capita per week')
for country, deathsDeltaPC, deathsDelta, pop, date in countryDeathsDeltaPC[0:20]:
    print("%-15s" % country, ': %10.1f %5d %10d %s' % (deathsDeltaPC, deathsDelta, pop, date.strftime("%Y-%m-%d")))

plt.show()
