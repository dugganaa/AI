import pandas as pd
'''
Probabilities and Rewards of Exercise/Rewards without
the probability of death

fit -> fit   | fit -> unfit
unfit -> fit | unfit -> unfit
'''
probrEx = [[(0.99, 8), (0.01, 8)],
           [(0.2, 0),  (0.8, 0)]]

probrRe = [[(0.7,10),(0.3,10)],
           [(0,5),   (1, 5)]]


'''
Probabilities and Rewards of Exercise/Rewards with
the probability of death

fit -> fit     | fit -> unfit   | fit -> death
unfit -> fit   | unfit -> unfit | unfit -> death
death -> death
'''
probrExDeath = [[(0.891, 8), (0.009, 8), (0.1, 0)],
                [(0.18, 0),  (0.72, 0),  (0.1, 0)],
                [(1, 0)]]

probrReDeath = [[(0.693,10),(0.297,10), (0.01, 0)],
                [(0,5),     (0.99, 5),  (0.01, 0)],
                [(1, 0)]]


#Discount Factor
gamma = 0.9

#iterations
n = 3

#utility function for single state change from s given action a
def util0(s,a,death):
    util = 0
    if death:
        if a == 0:
            for sprime in probrExDeath[s]:
                util = util + sprime[0] * sprime[1]
        elif a == 1:
            for sprime in probrReDeath[s]:
                util = util + sprime[0] * sprime[1]

    else:
        if a == 0:
            for sprime in probrEx[s]:
                util = util + sprime[0] * sprime[1]
        elif a == 1:
            for sprime in probrRe[s]:
                util = util + sprime[0] * sprime[1]
    return util


#Given current state s returns max expected reward (Value) across all actions
def maxRew(s,n,death):
    if n > 0:
        return max(utilnp1(s,0,n,death),utilnp1(s,1,n,death))
    else:
        return max(util0(s,0,death),util0(s,1,death))


#Utility function for n remaining iterations
#For a state s, current + future reward =
# q0 + discount factor * ((P(state changed) * a) + P(state did not change) * a)
# where a = action which suggests the highest expected reward
def utilnp1(s,a,n,death):
    futR = 0
    i = 0
    if death:
        if a == 0:
            for sprime in probrExDeath[s]:
                futR =  futR + sprime[0] * maxRew(i, n-1,death)
                i = i + 1

        elif a == 1:
            for sprime in probrReDeath[s]:
                futR = futR + sprime[0] * maxRew(i,n-1,death)
                i = i + 1
    else:
        if a == 0:
            for sprime in probrEx[s]:
                futR =  futR + sprime[0] * maxRew(i, n-1,death)
                i = i + 1

        elif a == 1:
            for sprime in probrRe[s]:
                futR = futR + sprime[0] * maxRew(i,n-1,death)
                i = i + 1

    return util0(s, a,death) + gamma * futR

#Given the Results from each iteration, create a list of the optimal policy for fit state
def policyListCreateFit(results):
    policyFit = []
    for i in range(0,n):
        if results[0][i] > results[2][i]:
            policyFit.append("Exercise")
        else:
            policyFit.append("Relax")
    return policyFit

#Given the Results from each iteration, create a list of the optimal policy for unfit state
def policyListCreateUnfit(results):
    policyUnfit = []
    for i in range(0,n):
        if results[1][i] > results[3][i]:
            policyUnfit.append("Exercise")
        else:
            policyUnfit.append("Relax")
    return policyUnfit


#Initialise results as a list of lists of all actions and states and their results
results = []
results_d = []
for _ in range(0,(len(probrEx)**2)):
    results.append([])
    results_d.append([])

#Iterate from 0 to n to determine the best policy
#Results are appended to the appropriate list within results/results_d
#Figures are rounded to 5 places
for x in range(0,n):
    if x == 0:
        for s in range(0,len(probrEx)):
            results[s].append(round(util0(s,0,False),5))
            results_d[s].append(round(util0(s,0,True),5))

        for s in range(0,len(probrRe)):
            results[s+2].append(round(util0(s,1,False),5))
            results_d[s+2].append(round(util0(s,1,True),5))

    else:
        for s in range(0,len(probrEx)):
            results[s].append(round(utilnp1(s,0,x,False),5))
            results_d[s].append(round(utilnp1(s,0,x,True),5))

        for s in range(0,len(probrRe)):
            results[s+2].append(round(utilnp1(s,1,x,False),5))
            results_d[s+2].append(round(utilnp1(s,1,x,True),5))


#Stored results in dataframes for tidiness when printing
df = pd.DataFrame({'state': ['fit', 'unfit'], 'exercise' : [results[0], results[1]],
                    'relax' : [results[2], results[3]]})
df.set_index('state', inplace=True)
print(df)
print(f"\nPolicy from fit state: {policyListCreateFit(results)}")
print(f"Policy from unfit state: {policyListCreateUnfit(results)}")


print("\n\nRewards when including the chance of death:\n")
df2 = pd.DataFrame({'state': ['fit', 'unfit'], 'exercise' : [results_d[0], results_d[1]],
                    'relax' : [results_d[2], results_d[3]]})
df2.set_index('state', inplace=True)
print(df2)
print(f"\nPolicy from fit state when death possible: {policyListCreateFit(results_d)}")
print(f"Policy from unfit state when death possible: {policyListCreateUnfit(results_d)}")
