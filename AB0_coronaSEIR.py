"""
Modelling of AB0 blood types influence.

https://old.reddit.com/r/COVID19/comments/fjzjpc/relationship_between_the_abo_blood_group_and_the/fkpwxs6/

Relationship between the ABO Blood Group and the COVID-19 Susceptibility
https://www.medrxiv.org/content/10.1101/2020.03.11.20031096v1

Inhibition of the interaction between the SARS-CoV spike protein and its cellular receptor by
anti-histo-blood group antibodies. https://www.ncbi.nlm.nih.gov/pubmed/18818423

# output
# blood types order: ['A', 'B', 'AB', '0']
# population BT distr.: [0.32 0.25 0.09 0.34] from paper (Wuhan, similar to "other areas")
# transm. coef.     peak   @   day      relative blood type distribution @ peak-day/2
# 1.0000            17174      55       [1. 1. 1. 1.]
# 0.7500            17073      55       [1.028 1.006 1.127 0.935]
# 0.5000            16615      56       [1.069 1.01  1.311 0.845]
# 0.2500            15223      60       [1.143 1.003 1.625 0.698]
# 0.1250            13453      65       [1.221 0.977 1.919 0.566]
# empirical relative BT distribution hospital: 1.21, 1.09, 1.48, 0.67 from paper ("overall")

"""

import numpy as np
np.set_printoptions(precision=3)
import scipy.integrate
import matplotlib.pyplot as plt
import matplotlib.widgets  # Cursor
import matplotlib.dates


def scale_tC(C):  # naive - adhere to blood type distribution?
    return C / np.mean(C)   # correct? little influence on BT distribution

def scaled_tC(c):
    tCr = tCMatch + c * tCDiff
    tCs = scale_tC(tCr)
    return tCs


# Susceptible X FROM Infected Y
# ['SAIA', 'SAIB', 'SAIC', 'SAI0'],  # C = AB; IA --> SA, IB --> SA, IAB --> SA ...
# ['SBIA', 'SBIB', 'SBIC', 'SBI0'],
# ['SCIA', 'SCIB', 'SCIC', 'SCI0'],
# ['S0IA', 'S0IB', 'S0IC', 'S0I0'],

DEFAULTCROSSINFECTIONFACTOR = 0.65  # CIF e.g. IA --> SB 0.5  (direct, e.g. IA --> SA is 1.0)

d = 1.0  # Is IA --> SA more easy than I0 --> SA ?

# 0.9: 0.56 1.6e-6
# 0.8: 0.59 3.8e-7
# 0.7: 0.61 1.3e-7
# 0.6: 0.62 7e-8
# 0.5: 0.45 ~2e-4

tCMatch = np.array([
    [1, 0, 0, d],
    [0, 1, 0, d],
    [1, 1, 1, d],
    [0, 0, 0, d], ], dtype='float64')

# tCMatch[2,0] = 0.9  # in reality there are two A subtypes A1 and A2 which in particular might make AB do a bit better

tCDiff = 1 - tCMatch


print("Default transmission Matrix:\n", scaled_tC(DEFAULTCROSSINFECTIONFACTOR))


bloodTypes = ['A', 'B', 'AB', '0']
if __name__ == '__main__':
    BT = np.array([0.32, 0.25, 0.09, 0.34])
    # BT = np.array([0.25, 0.25, 0.25, 0.25])
    assert(sum(BT) == 1.0)
    print('blood types order:', bloodTypes)
    print('population BT distr.:', BT, 'from paper (Wuhan, similar to "other areas")')

    E0 = np.copy(BT)  # np.array([0.25, 0.25, 0.25, 0.25])  # little influence

    population = 100000
    S0 = BT * population - E0

daysTotal = 130  # total days to model
days0 = 129

r0 = 3.0  # https://en.wikipedia.org/wiki/Basic_reproduction_number
r1 = 1.0  # reproduction number after quarantine measures - https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3539694
          # it seems likely that measures will become more restrictive if r1 is not small enough

timePresymptomatic = 2.5  # almost half infections take place before symptom onset (Drosten) https://www.medrxiv.org/content/10.1101/2020.03.08.20032946v1.full.pdf

# I in this model is maybe better described as 'Infectors'? Event infectious persons in quarantine do not count.
sigma = 1.0 / (5.2 - timePresymptomatic)  # The rate at which an exposed person becomes infectious.  symptom onset - presympomatic
# for SEIR: generationTime = 1/sigma + 0.5 * 1/gamma = timeFromInfectionToInfectiousness + timeInfectious  https://en.wikipedia.org/wiki/Serial_interval
generationTime = 4.6  # https://www.medrxiv.org/content/10.1101/2020.03.05.20031815v1  http://www.cidrap.umn.edu/news-perspective/2020/03/short-time-between-serial-covid-19-cases-may-hinder-containment
gamma = 1.0 / (2.0 * (generationTime - 1.0 / sigma))  # The rate an infectious is not recovers and moves into the resistant phase. Note that for the model it only means he does not infect anybody any more.

beta0 = r0 * gamma  # The parameter controlling how often a susceptible-infected contact results in a new infection.
beta1 = r1 * gamma  # beta0 is used during days0 phase, beta1 after days0


def model(Y, x, N, beta0, days0, beta1, gamma, sigma, tCm):
    # :param array x: Time step (days)
    # :param int N: Population
    # :param float beta: The parameter controlling how often a susceptible-infected contact results in a new infection.
    # :param float gamma: The rate an infected recovers and moves into the resistant phase.
    # :param float sigma: The rate at which an exposed person becomes infective.

    Y = np.reshape(Y, (4, 4))
    S, E, I, R = Y
    beta = beta0 if x < days0 else beta1
    FI = beta * I / N  # 'Force of infection'  https://www.researchgate.net/figure/An-example-of-a-two-class-age-structured-SIR-model-with-parameters-for-a-typical-human_fig3_259825206

    dS = - np.sum(np.outer(S, FI) * tCm, axis=1)
    dE = np.sum(np.outer(S, FI) * tCm, axis=1) - sigma * E
    dI = sigma * E - gamma * I
    dR = gamma * I

    return np.reshape(np.array([dS, dE, dI, dR]), (16,))


def solve(model, S0, E0, beta0, days0, beta1, gamma, sigma, tCs, daysTotal):
    I0 = np.array([0, 0, 0, 0])
    R0 = np.array([0, 0, 0, 0])
    population = np.sum(S0 + E0 + I0 + R0)

    X = np.arange(daysTotal)  # time steps array
    N0s = S0, E0, I0, R0  # S, E, I, R at initial step
    N0s = np.array(N0s)
    N0 = N0s.reshape((16,))
    y_data_var = scipy.integrate.odeint(model, N0, X, args=(population, beta0, days0, beta1, gamma, sigma, tCs))
    y_data_var = y_data_var.reshape((daysTotal, 4, 4))

    S = y_data_var[:,0,:].T
    E = y_data_var[:,1,:].T
    I = y_data_var[:,2,:].T
    R = y_data_var[:,3,:].T

    return X, S, E, I, R  # note these are all arrays


def solve_simple(S0, E0, c=DEFAULTCROSSINFECTIONFACTOR):
    tCs = scaled_tC(c)
    return solve(model, S0, E0, beta0, days0, beta1, gamma, sigma, tCs, daysTotal)


if __name__ == '__main__':  # do not run the stuff below if this file is imported in other files
    # Plot and print
    fig = plt.figure(dpi=75, figsize=(20, 16))
    ax = fig.add_subplot(211)

    print('transm. coef.     peak   @   day      relative blood type distribution @ peak-day/2')
    for c in [1.0, 0.75, 0.5, 0.25, 0.125]:
        tCs = scaled_tC(c)

        X, S, E, I, R = solve(model, S0, E0, beta0, days0, beta1,
                              gamma, sigma, tCs, daysTotal)

        ax.plot(X, np.sum(I, axis=0), alpha=0.6, lw=3, label='Infected, transmission coefficient: %.1f' % c)

        if c in [0.125]:  # , 1.0]:
            for i, col in ((3, 'purple'), (1, 'red'), (2, 'blue'), (0, 'orange')):
                ax.plot(X, I[i], color=col, alpha=0.5, lw=1,
                        label='Infected, t.c.: %.1f b.t.: %s' % (c, bloodTypes[i]))

        i = np.argmax(np.sum(I, axis=0))  # peak day, fixed day gives similar results
        print("%6.4f         %8d    %4d      " % (c, np.sum(I[:, i]), i), I[:, int(i / 2)] / np.sum(I[:, int(i / 2)]) / BT)

    ax.grid(linestyle=':')
    ax.set_xlabel('Time /days')
    legend = ax.legend(title='COVID-19 SEIR model - blood types distribution (beta)')

    ax = fig.add_subplot(212)

    C = np.arange(0.1, 1.01, 0.01)
    BD = []
    for c in C:
        tCs = scaled_tC(c)

        X, S, E, I, R = solve(model, S0, E0, beta0, days0, beta1,
                              gamma, sigma, tCs, daysTotal)

        BD.append(I[:, int(i / 2)] / np.sum(I[:, int(i / 2)]) / BT)

    BD = np.array(BD)
    for i, bd in enumerate(BD.T):
        ax.plot(C, bd, alpha=0.5, label="blood type: " + bloodTypes[i])

    ax.grid(linestyle=':')
    legend = ax.legend(title='COVID-19 SEIR model (beta)\nrelative blood types distribution over transmission coefficient')
    ax.set_xlabel('Transmission coefficient')
    ax.set_xlim(1.0, 0.0)

    cursor = matplotlib.widgets.Cursor(ax, color='black', linewidth=1)

    print('empirical relative BT distribution hospital: 1.21, 1.09, 1.48, 0.67 from paper ("overall")')

    if 1:
        plt.show()
    else:
        plt.savefig('AB0.png')
