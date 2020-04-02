# https://old.reddit.com/r/COVID19/comments/fjzjpc/relationship_between_the_abo_blood_group_and_the/fkpwxs6/
# Relationship between the ABO Blood Group and the COVID-19 Susceptibility https://www.medrxiv.org/content/10.1101/2020.03.11.20031096v1
# Inhibition of the interaction between the SARS-CoV spike protein and its cellular receptor by anti-histo-blood group antibodies. https://www.ncbi.nlm.nih.gov/pubmed/18818423

# todo: order blood types as in paper

import math
import numpy as np
np.set_printoptions(precision=3)
import scipy.integrate
import matplotlib.pyplot as plt
import matplotlib.widgets  # Cursor
import matplotlib.dates

def scale_tC(C):  # naive - adhere to blood type distribution?
    return C/ np.mean(C)   # correct? little influence on BT distribution

# ['S0I0', 'S0IA', 'S0IB', 'S0IC'],  # C = AB; I0 infects S0, IA --> S0, IB --> S0, IAB --> S0
# ['SAI0', 'SAIA', 'SAIB', 'SAIC'],  # I0 --> SA, IA --> SA, ...
# ['SBI0', 'SBIA', 'SBIB', 'SBIC'],
# ['SCI0', 'SCIA', 'SCIB', 'SCIC']

tCMatch = np.array([
    [1, 0, 0, 0],
    [1, 1, 0, 0],
    [1, 0, 1, 0],
    [1, 1, 1, 1],], dtype='float64')

tCDiff = 1 - tCMatch

bloodTypes = ['0', 'A', 'B', 'AB']  # in reality there are two A subtypes A1 and A2 which in particular might make AB do a bit better
BT = np.array([0.34, 0.32, 0.25, 0.09])
#BT = np.array([0.25, 0.25, 0.25, 0.25])
assert(sum(BT) == 1.0)
print('population BT distribution:', BT, ' 0 A B AB from paper (Wuhan, similar to other areas)')

E0 = np.copy(BT)  #np.array([0.25, 0.25, 0.25, 0.25])  # little influence
I0 = np.array([0, 0, 0, 0])
R0 = np.array([0, 0, 0, 0])

population = 100000
S0 = BT * population


#E0 = 1  # exposed at initial time step
daysTotal = 130  # total days to model
dataOffset = 'auto'  # position of real world data relative to model in whole days. 'auto' will choose optimal offset based on matching of deaths curves
days0 = 129  # Germany:60 France: Italy:65? Spain:71? 'all'butChina:68? days before lockdown measures - you might need to adjust this according to output "lockdown measures start:"

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

    Y = np.reshape(Y, (4,4))
    S, E, I, R = Y
    beta = beta0 if x < days0 else beta1
    FI = beta * I / N  # 'Force of infection'  https://www.researchgate.net/figure/An-example-of-a-two-class-age-structured-SIR-model-with-parameters-for-a-typical-human_fig3_259825206

    dS = - np.sum(np.outer(S, FI) * tCm, axis=1)
    dE = np.sum(np.outer(S, FI) * tCm, axis=1) - sigma * E
    dI = sigma * E - gamma * I
    dR = gamma * I

    return np.reshape(np.array([dS, dE, dI, dR]), (16,))

def solve(model, population, E0, beta0, days0, beta1, gamma, sigma, tCs):
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

# Plot
fig = plt.figure(dpi=75, figsize=(20,16))
ax = fig.add_subplot(111)
for c in [1.0, 0.75, 0.5, 0.25, 0.125]:
    tCr = tCMatch + c * tCDiff
    #tCn = tCr
    
    tCn = scale_tC(tCr)
    
    X, S, E, I, R = solve(model, population, E0, beta0, days0, beta1,
                              gamma, sigma, tCn)
    IallBt = np.sum(I, axis=0)
    ax.plot(X, IallBt, alpha=0.6, lw=3, label='Infected, transmission coefficient: %.1f' % c)
    
    if c in [1.0, 0.125]:
        for i, col in ((3, 'purple'), (1, 'red'), (2, 'blue'), (0, 'orange')):
            ax.plot(X, I[i], color=col, alpha=0.5, lw=1,
                    label='Infected, t.c.: %.1f b.t.: %s' % (c, bloodTypes[i]))
    
    i = np.argmax(np.sum(I, axis=0))  # peak day, fixed day gives similar results
    print("c:%6.4f %8d     day:%4d    BT dist.:" % (c, np.sum(I[:, i]), i), I[:, int(i/2)] / np.sum(I[:, int(i/2)]) / BT)


ax.set_xlabel('Time /days')
ax.grid(linestyle=':')
legend = ax.legend(title='COVID-19 SEIR model - blood types (beta)')
legend.get_frame().set_alpha(0.5)
cursor = matplotlib.widgets.Cursor(ax, color='black', linewidth=1 )

print('empirical BT distribution hospital: 0.67, 1.21, 1.09, 1.48  0 A B AB from paper (overall)')

if 1:
    plt.show()
else:
    plt.savefig('model_run.png')
