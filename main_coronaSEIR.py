import math
import numpy as np
import scipy.integrate
import matplotlib.pyplot as plt
import matplotlib.widgets  # Cursor

import world_data

COUNTRY = 'Italy'  #South Korea'  #  e.g. 'France'  'Republic of Korea' 'Italy' 'Germany' 
PROVINCE = 'all'  #'all'  # 'Hubei'

populations = {'Germany' : 81E6, 'France' : 67E6, 'Italy' : 61E6, 'Iran' : 81E6,
               'Mainland China' : 1438E6, 'Hubei' : 59E6, 'Republic of Korea' : 51E6}
if PROVINCE == 'all':
    population = populations[COUNTRY]
else:
    population = populations[PROVINCE]

intensiveUnits = 14000 / 2  # ICU units available  # Germany: 28000  


logPlot = True

E0 = 1  # exposed at initial time step

days = 165  # total days to model

dataOffset = 25 # how many days will the real world country data be delayed in the model

days0 = dataOffset + 35  # days before lockdown measures

beta0 = 1.0 / 2.5  # The parameter controlling how often a susceptible-infected contact results in a new infection.
beta1 = beta0 / 4  # beta0 is used during days0 phase, beta1 after days0

gamma = 1.0 / (10 + 3)  # The rate an infected recovers and moves into the resistant phase.
sigma = 1.0 / (5 - 3)  # The rate at which an exposed person becomes infective.
  # https://www.reddit.com/r/COVID19/comments/fgark3/estimating_the_generation_interval_for_covid19/
  # three days shorter because it seems there are earlier infections, goes into gamma

noSymptoms = 0.2  # https://www.reddit.com/r/COVID19/comments/ffzqzl/estimating_the_asymptomatic_proportion_of_2019/
findRatio = (1 - noSymptoms) / 4  # a lot of the mild cases will go undetected  assuming 100% correct tests

timeInHospital = 12
timeInfected = 1.0 / gamma

# lag, whole days
communicationLag = 2
testLag = 8
symptomToHospitalLag = 5

icuRate = 0.02
infectionFatalityRateA = 0.01
infectionFatalityRateB = infectionFatalityRateA * 2  # higher lethality without ICU - by how much?

r0 = beta0 / gamma  # somehow an r0 of 3.0 seems to low
r1 = beta1 / gamma

print("r0: %.2f" % r0, "   r1: %.2f" % r1)

# https://hal.archives-ouvertes.fr/hal-00657584/document page 13
s1 = 0.5 * (-(sigma + gamma) + math.sqrt((sigma + gamma) ** 2 + 4 * sigma * gamma * (r0 -1)))
print("doubling0 every ~%.1f" % (math.log(2.0, math.e) / s1), "days")

def model(Y, x, N, beta0, days0, beta1, gamma, sigma):
    # :param array x: Time step (days)
    # :param int N: Population
    # :param float beta: The parameter controlling how often a susceptible-infected contact results in a new infection.
    # :param float gamma: The rate an infected recovers and moves into the resistant phase.
    # :param float sigma: The rate at which an exposed person becomes infective.

    S, E, I, R = Y

    beta = beta0 if x <= days0 else beta1

    dS = - beta * S * I / N
    dE = beta * S * I / N - sigma * E
    dI = sigma * E - gamma * I
    dR = gamma * I
    return dS, dE, dI, dR


def solve(model, population, E0, beta0, days0, beta1, gamma, sigma):
    X = np.arange(days)  # time steps array
    N0 = population - E0, E0, 0, 0  # S, E, I, R at initial step

    y_data_var = scipy.integrate.odeint(model, N0, X, args=(population, beta0, days0, beta1, gamma, sigma))

    S, E, I, R = y_data_var.T  # transpose and unpack
    return X, S, E, I, R  # note these are all arrays

X, S, E, I, R = solve(model, population, E0, beta0, days0, beta1, gamma, sigma)

F = I * findRatio
H = I * icuRate * timeInHospital / timeInfected
P = I / population * 1000000 # probability of random person to be infected

# estimate deaths from recovered
D = np.arange(days)
RPrev = 0
DPrev = 0
for i, x in enumerate(X):
    IFR = infectionFatalityRateA if H[i] <= intensiveUnits else infectionFatalityRateB
    D[i] = DPrev + IFR * (R[i] - RPrev)
    RPrev = R[i]
    DPrev = D[i]

# add delays
F = world_data.delay(F, symptomToHospitalLag + testLag + communicationLag)  # found in tests; from I
H = world_data.delay(H, symptomToHospitalLag)  # ICU  from I
D = world_data.delay(D, timeInHospital + communicationLag)  # deaths  from R


def print_info(i):
    print("day %d" % i)
    print(" Infected: %d" % I[i], "%.1f" % (I[i] * 100.0 / population))
    print(" Infected found: %d" % F[i], "%.1f" % (F[i] * 100.0 / population))
    print(" Hospital: %d" % H[i], "%.1f" % (H[i] * 100.0 / population))
    print(" Recovered: %d" % R[i], "%.1f" % (R[i] * 100.0 / population))
    print(" Deaths: %d" % D[i], "%.1f" % (D[i] * 100.0 / population))

print_info(days0)
print_info(days - 1)

# Plot
fig = plt.figure(figsize=(10,10), dpi=200)
ax = fig.add_subplot(111)
if logPlot:
    ax.set_yscale("log", nonposy='clip')
    
#ax.plot(X, S, 'b', alpha=0.5, lw=2, label='Susceptible')
#ax.plot(X, E, 'y', alpha=0.5, lw=2, label='Exposed')
ax.plot(X, I, 'r--', alpha=0.5, lw=1, label='Infected')
ax.plot(X, F, color='orange', alpha=0.5, lw=1, label='Found')
ax.plot(X, H, 'r', alpha=0.5, lw=2, label='ICU')
#ax.plot(X, R, 'g', alpha=0.5, lw=1, label='Recovered with immunity')
#ax.plot(X, P, 'c', alpha=0.5, lw=1, label='Probability of infection')
ax.plot(X, D, 'k', alpha=0.5, lw=1, label='Deaths')

ax.plot([min(X), max(X)], [intensiveUnits, intensiveUnits], 'b-.', alpha=0.5, lw=1, label='Number of ICU available')


# actual country data
XCDR_data = np.array(world_data.get_country_xcdr(COUNTRY, PROVINCE, dateOffset=dataOffset))

ax.plot(XCDR_data[:,0], XCDR_data[:,1], 'o', color='orange', alpha=0.5, lw=1, label='cases actually detected in tests')
ax.plot(XCDR_data[:,0], XCDR_data[:,2], 'x', color='black', alpha=0.5, lw=1, label='actually deceased')

#print(XCDR_data[0:30])

ax.set_xlabel('Time /days')
ax.set_ylabel('Number (1000s)')
ax.set_ylim(bottom=1.0)

ax.grid(b=True, which='major', c='w', lw=2, ls='-')
legend = ax.legend(title='COVID-19 SEIR model: ' + COUNTRY + " " + PROVINCE +
                   ' %dk' % (population / 1000) + ' (beta)')
legend.get_frame().set_alpha(0.5)
for spine in ('top', 'right', 'bottom', 'left'):
    ax.spines[spine].set_visible(False)
cursor = matplotlib.widgets.Cursor(ax, color='black', linewidth=1 )
plt.show()
#plt.savefig('model_run.png')