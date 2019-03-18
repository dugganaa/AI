# Trinity College Dublin CS3061 Artificial Intelligence Assignment
## Markov Decision Process

### Given the following states and actions:

S = {fit, unfit}

A = {exercise, relax}

Probability-reward matrices (p(s,a,s'),r(s,a,s'))

|exercise |  fit       |  unfit
|:-------:|:----------:|:------:|
|fit      |   .99, 8   |  .01, 8
|unfit    |   .2, 0    |  .8, 0

|relax    |  fit       |  unfit |
|:-------:|:----------:|:------:|
|fit      |   .7, 10   |  .3, 10|
|unfit    |  0, 5      |  1, 5  |

### Upon completion of the above, the assignment also specifies another state in S: death

p(s,exercise,dead) = 1/10 for s ∈ S

p(s,exercise,s') = 9p(s,exercise,s')/10 for s,s' ∈ S

p(s,relax,dead) = 1/100 for s ∈ S

p(s,relax,s') = 99p(s,exercise,s')/100 for s,s' ∈ S


### Death is considered a sink:

p(dead, a, dead) = 1 for a ∈ A

r(s, a, dead) = 0 for s ∈ S, a ∈ A .

