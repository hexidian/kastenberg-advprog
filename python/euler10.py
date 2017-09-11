import math
def sprime(n):
    stop = int(math.sqrt(n))
    if n%2==0: return False
    for i in range(3,stop,2):
        if n%i==0: return False
    return True

def primeRange(n):
    workingList = [2]
    for i in range(3,n,2):
        if sprime(i): workingList.append(i)
    return workingList
def bprime(factors,n):
    for i in factors:
        if n%i==0:
            return False
    return True
def main():
    limit = input("what number should I go up to?\n")
    maybeFactors = primeRange(int(math.sqrt(n)))
    total = 2
    for i in range(3,limit,2):
        if bprime(maybeFactors,i): total+=i
    print "the total of all primes up to",limit,"is",total
