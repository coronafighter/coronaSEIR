#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Looking for correlation between ABH SEIR model with country BT data to real Covid-19 data."""


CROSSINFECTIONFACTOR = 0.65
MINIMUMFATALITIES = 1000

# 1.0 r:0.27 p: ~3 e-2
# r ~ 0.53
# 0.9 7 e-6
# 0.8 3 e-6
# 0.7 5 e-6
# 0.6 6 e-6
# 0.5 8 e-6

# 0.95/0.95 0.52 1e-6   CIF & factor d
# 0.9/0.9 0.54 3.7e-7
# 0.8/0.8 0.54 2.7e-7
# 0.7/0.7 0.57 4.7e-8
# 0.6/0.6 0.57 5.4e-8
# 0.5/0.5 0.44 6e-5

import numpy as np
np.set_printoptions(precision=3)

import matplotlib.pyplot as plt
# from scipy.optimize import curve_fit
import scipy.stats

import world_data
import blood_type_country_models
import population


def line(X, a, b):
    return a * X + b

def normalize(D, text="", factor=100):
    maxV = max(D.values())
    for key in D.keys():
        D[key] = D[key] * 1.0 * factor / maxV
        if text:
            print(text, key, D[key])
    return D


if __name__ == '__main__':
    # prepare
    countries, provinces = world_data.get_countries_provinces()
    blood_type_country_models.run(CROSSINFECTIONFACTOR)

    # # real world data, cases and fatalities
    # how bad was a country hit?
    btdResults = blood_type_country_models.results
    targets = []
    for country in countries:
        if country in ["China", "South Korea"]:
            continue
        XCDR_data = np.array(world_data.get_country_xcdr(country, province='all',
                             returnDates=False, verbose=False))
        Y = XCDR_data[:, 2]
        if Y[-1] < MINIMUMFATALITIES:
            print("skipped", country, Y[-1])
            continue
        for r in btdResults:  # todo: make nicer
            if country == r[0]:
                targets.append(r)
    targets = sorted(targets, key=lambda x: x[1])
    for r in targets:
        print("%35s %8i" % (r[0], r[1]), r[2])

    countryData = blood_type_country_models.countryDataPBTD

    dataSeverities = {}
    for target in targets:
        country = target[0]
        if country in ['Diamond Princess', 'Zimbabwe', 'China']:
            continue
        XCDR_data = np.array(world_data.get_country_xcdr(country, province='all',
                                                         returnDates=False, verbose=False))
        Y = XCDR_data[:, 2]
        # adjust for country population
        pop = population.get_population(country)
        dataSeverities[country] = 1000.0 * Y[-1] / pop

    dataSeverities = normalize(dataSeverities, "real data:")

    # # model severity calculated using country blood type data
    # how bad would a country be hit according to blood type hypothesis?
    modelSeverities = {}
    for country in countryData:
        I = np.sum(countryData[country]['I'], axis=0)
        modelSeverities[country] = max(I)  # model peak

        # fit does not make a big difference but makes things a lot more complicated so
        # it is not currently being used
        # ijMin, sMin, popt, S, SX = opt_fit(X, I)  #, stepsize=8)
        # modelSeverities[country] = (ijMin, sMin, popt, S, SX)

    modelSeverities = normalize(modelSeverities, "model:")

    # naming fixes
    modelSeverities['US'] = modelSeverities['United States']
    modelSeverities['South Korea'] = modelSeverities['Korea']

    # # plot correlation
    fig, ax1 = plt.subplots(constrained_layout=True)
    ax1.grid(linestyle=':')

    X, Y = [], []
    for country in dataSeverities:
        x = dataSeverities[country]
        y = modelSeverities[country]
        print("%40s, %.3f %.3f" % (country, x, y))

        X.append(x)
        Y.append(y)

        ax1.plot(x, y, 'bo', label=country, alpha=0.5)
        ax1.annotate(country, (x, y))

    linReg = scipy.stats.linregress(X, Y)
    ax1.plot(np.linspace(0.05, int(max(X)), 50), line(np.linspace(0.05, int(max(X)), 50),
             linReg.slope, linReg.intercept))
    s = ("linReg: r: %.3f" % linReg.rvalue +
         " p: %.3E" % linReg.pvalue +
         " stderr: %.3f " % linReg.stderr)
    print(s)
    ax1.set_xlabel('real world data severity: deaths per capita normalized\n' + s)
    ax1.set_ylabel('ABH model severity (peak height normalized)')

    plt.show()
