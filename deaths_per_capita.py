import numpy as np
import matplotlib.pyplot as plt

import population
import world_data

countries, provinces = world_data.get_countries_provinces()
countryPopulation = population.get_all_population_data()

countryDeaths = []
for country in countries:
    try:
        if countryPopulation[country] < 1000000:
            continue
        XCDR_data = np.array(world_data.get_country_xcdr(country))
        cases = int(XCDR_data[-1, 1])  # last row, third column
        deaths = int(XCDR_data[-1, 2])  # last row, third column
        if deaths < 10:
            continue
        recovered = int(XCDR_data[-1, 3])  # last row, third column            
        countryDeaths.append((country, cases, deaths, recovered))

    except:
        print("fail: ", country)

countryDeathsPC = []
for ccdr in countryDeaths:
    country, cases, deaths, recovered = ccdr
    try:
        pop = population.get_population(country)
        countryDeathsPC.append((country, deaths * 1.0e6 / pop, deaths, pop))
        #countryDeathrate.append((country, 100.0 * deaths / cases, deaths, pop))
    except KeyError:
        print("fail: ", country)

print()
countryDeathsPC = sorted(countryDeathsPC, key = lambda x: x[1])  # sort by second subitem
countryDeathsPC.reverse()  # in place


dCountryDeathsPCXY = {}
for country, trash, trash, trash in countryDeathsPC[0:20]:
    XCDR_data = np.array(world_data.get_country_xcdr(country))
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
for country, deathsPC, deaths, pop in countryDeathsPC[0:20]:
    print("%-15s" % country, ': %10.1f %5d %10d' % (deathsPC, deaths, pop))

plt.show()