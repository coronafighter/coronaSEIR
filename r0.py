#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

import world_data
import shared


COUNTRY = 'all'
PROVINCE = 'all'
EXCLUDECOUNTRIES = ['China'] if COUNTRY == 'all' else []  # massive measures early on
#EXCLUDECOUNTRIES = []

XCDR_data = np.array(world_data.get_country_xcdr(COUNTRY, PROVINCE,
                                                 excludeCountries=EXCLUDECOUNTRIES, returnDates=True))


C = XCDR_data[:,1]  # cases
D = XCDR_data[:,2]  # deaths


INTERVAL = 4  # days


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

cR = calc_R(C)
dR = calc_R(D)

cR7 = shared.moving_average(cR, n=7, noRightZero=True)
dR7 = shared.moving_average(dR, n=7, noRightZero=True)

print("current 7 day moving averages R: cases %.2f   deaths %.2f" % (cR7[-5], dR7[-5]))

fig = plt.figure(dpi=75, figsize=(20,16))
ax = fig.add_subplot(111)
ax2 = ax.twinx()
ax2.set_yscale("log", nonposy='clip')

ax.grid(linestyle=':')

ax.plot(cR, color='orange', alpha=0.2, lw=1)
ax.plot(dR, color='black', alpha=0.2, lw=1)

ax.plot(cR7, color='orange', alpha=0.5, lw=2, marker=None)
ax.plot(dR7, color='black', alpha=0.5, lw=2, marker=None)


ax2.plot(C, marker='o', color='orange', alpha=0.5, lw=1)
ax2.plot(D, marker='x', color='black', alpha=0.5, lw=1)
plt.show()