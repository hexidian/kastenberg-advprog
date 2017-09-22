import math
def isAbundant(n):
    properDivisors = [1]
    for i in range(2,int(math.sqrt(n))+1):
        if n%i==0:
            properDivisors.append(i)
            if i**2!=n: properDivisors.append(n/i)
    if sum(properDivisors)>n: return True
    return False

def abundRange(n):
    abundants = []
    for i in range(2,n):
        if isAbundant(i): abundants.append(i)
    return abundants

def isAbundSum(n,abundants):
    for i in abundants:
        if i>n:
            break
        for j in abundants:
            if i+j==n:
                return True
            if i+j>n:
                break
    return False

def abundSumsInRange(n):
    abundants = abundRange(n)
    abundSums = []
    for i in range(2,n):
        if isAbundSum(i,abundants): abundSums.append(i)
    return abundSums

def highestNonAbundantSum(n):
    abundants = abundRange(n)
    top = 0
    for i in range(2,n):
        if not isAbundSum(i,abundants): top = i
    return top

print highestNonAbundantSum(5000)
