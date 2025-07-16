def factorial(n: int):
    if n <= 1:
        return 1
    else:
        result = 1
        for i in range(1, n+1):
            result *= i
        return result

def binomial_dist(n: int, p: float, x: int):
    nCx = factorial(n) / (factorial(x) * factorial(n - x))
    return nCx * (p ** x) * ((1 - p) ** (n - x))

def cdf(n: int, p: float, x: int):
    probability = 0
    for i in range(0, x + 1):
        probability = probability + binomial_dist(n, p, i)
    return probability

def binomial_test():
    tails: int = int(input("1 tail? [1]\n2 tail? [2]\n")) # 1 tailed test or 2 tailed?

    significance_level: float = float(input("Enter significance level: "))
    p: float = float(input("Enter probability of success (p): ")) # probability of success
    n: int = int(input("Enter number of trials: ")) # number of trials
    x: int = int(input("Enter number of observations: ")) # observed

    if tails == 1:
        change = input("Greater than [G]\nor\nLess than? [L]\n") # is p > a or p < a?

        if change.upper() == 'L':
            print(f"Model: X~B({n}, {p})")
            print(f"H0: p = {p}\nH1: p < {p}")

            # test against sigificance level
            if cdf(n, p, x) < significance_level:
                print("Reject H0") # my bad gang
                print("Accept H1") # im retarded
            else:
                print("Accept H0") # fuck you im always right

        # same shit again for > sign        
        elif change.upper() == 'G':
            print(f"Model: X~B({n}, {p})")
            print(f"H0: p = {p}\nH1: p > {p}")

            # test against sigificance level
            if (1 - cdf(n, p, x-1)) < significance_level:
                print("Reject H0") 
                print("Accept H1") 
            else:
                print("Accept H0")

    elif tails == 2:
        print(f"Model: X~B({n}, {p})")
        print(f"H0: p = {p}\nH1: p != {p}")

        # test against significance level
        if (cdf(n, p, x) < significance_level / 2):
            print("Reject H0") 
            print("Accept H1") 
        else:
            print("Accept H0")

    else:
        # tell the user to stop being silly
        raise ValueError("You can only have 1 or 2 tails. If you want 1 tailed test, enter 1, otherwise enter 2")


binomial_test()