# binomial-test

This is a stats engine that carries out hypothesis tests for the binomial distribution, both 1 and 2 tailed.
<br />
<br />

## Binomial Distribution

The binomial distribution is as follows:

$$\text{For the binomial distribution } X \sim B(n,p)$$

**Probability Mass Function:**

$$P(X=x) = \binom{n}{x} p^x (1-p)^{n-x} = \frac{n!}{x!(n-x)!} p^x (1-p)^{n-x}$$

**Cumulative Distribution Function:**

$$P(X \leq x) = \sum_{i=0}^{x} \binom{n}{i} p^i (1-p)^{n-i} = \sum_{i=0}^{x} \frac{n!}{i!(n-i)!} p^i (1-p)^{n-i}$$


<br />
i wrote this latex to make the docs look cool, really and truly theres nothing mathematically exciting going on here, now fuck off
