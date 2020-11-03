#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

import world_data
import shared

INTERVAL = 4  # days

COUNTRY = 'all'
PROVINCE = 'all'
EXCLUDECOUNTRIES = ['China'] if COUNTRY == 'all' else []  # massive measures early on
#EXCLUDECOUNTRIES = []

XCDR_data = np.array(world_data.get_country_xcdr(COUNTRY, PROVINCE,
                                                 excludeCountries=EXCLUDECOUNTRIES, returnDates=True))

C = XCDR_data[:,1]  # cases
D = XCDR_data[:,2]  # deaths

deltaC = np.diff(C)  # new per day
deltaD = np.diff(D)

def calc_R(Y):
    R = []
    for i, y in enumerate(Y):
        index = i + INTERVAL
        if index >= len(Y):  # can't calculate R yet as resulting cases/deaths value not yet available
            continue
        try:
            r = Y[index] / y
        except ZeroDivisionError:
            r = 0
        R.append(r)
    return R

smoothDeltaC = shared.moving_average(deltaC, n=7)  # smooth out weekly swing
smoothDeltaD = shared.moving_average(deltaD, n=7)

cR = calc_R(smoothDeltaC)
dR = calc_R(smoothDeltaD)

smoothCR = shared.moving_average(cR, n=1)
smoothDR = shared.moving_average(dR, n=1)

print("experimental!")
print("assumed interval:", INTERVAL)
print("filtered moving averages R: cases %.2f   deaths %.2f" % (smoothCR[-1], smoothDR[-1]))

fig = plt.figure(dpi=75, figsize=(20,16))
ax = fig.add_subplot(111)
ax.set_ylim(top=7.0)
ax2 = ax.twinx()
ax2.set_ylabel('NEW PER DAY')
ax2.set_yscale("log", nonpositive='clip')

ax.grid(linestyle=':')

ax.plot(cR, color='orange', alpha=0.2, lw=1)
ax.plot(dR, color='black', alpha=0.2, lw=1)

ax.plot(smoothCR, color='orange', alpha=0.5, lw=2, marker=None)
ax.plot(smoothDR, color='black', alpha=0.5, lw=2, marker=None)

ax2.plot(deltaC, marker='o', color='orange', alpha=0.5, lw=0)
ax2.plot(deltaD, marker='x', color='black', alpha=0.5, lw=0)

ax2.plot(smoothDeltaC, marker='', color='orange', alpha=0.5, lw=1)
ax2.plot(smoothDeltaD, marker='', color='black', alpha=0.5, lw=1)

plt.show()
