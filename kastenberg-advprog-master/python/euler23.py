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
    for i in range(0,len(abundants)):
        if abundants[i]>n:
            break
        for j in range(i,len(abundants)):
            if abundants[i]+abundants[j]==n:
                return True
            if abundants[i]+abundants[j]>n:
                break
    return False

def abundSumsInRange(n):
    abundants = abundRange(n)
    abundSums = []
    for i in range(2,n):
        if isAbundSum(i,abundants): abundSums.append(i)
        if i%100==0: print "at",i
    return abundSums

def nonAbundantSumsRange(n):
    abundants = abundRange(n)
    nonAbundSums = []
    for i in range(2,n):
        if not isAbundSum(i,abundants): nonAbundSums.append(i)
        if i%100==0: print "at",i
    return sum(nonAbundSums)

def highestNonAbundantSum(n):
    abundants = abundRange(n)
    top = 0
    for i in range(2,n):
        if not isAbundSum(i,abundants): top = i
    return top

print abundSumsInRange(28123)
