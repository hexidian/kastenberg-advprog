import random
class Species:

    def __init__(self,evaluate,values,genSize,randomness):
        self.evaluate = evaluate

        self.values = values    #this will be a list of whatever values are relevant to the current problem being solved. The list will be the max values (minimum is assumed 0)
                                #NOTE: remember that these values can only be integers, so don't make the range too small; use units accordingly (i.e. 1200 mL, not 1.2 L)

        self.genSize = genSize

        self.randomness = randomness

        #each citizen of a generation will simply be a list of values

        self.currentGeneration = [[random.randint(0,values[i]) for i in range(len(values))] for j in range(genSize)] #just establishes a first generation

    def evolve(self,generations):
        bestTwo = [[self.evaluate(self.currentGeneration[0]),self.currentGeneration[0]],[self.evaluate(self.currentGeneration[1]),self.currentGeneration[1]]]
        evalutedGeneration = []
        for generation in range(generations):
            for citizen in self.currentGeneration:
                curEval = self.evaluate(citizen)
                evaluatedCitizen = [curEval,citizen]
                if curEval > bestTwo[0][0]:
                    bestTwo[1] = bestTwo[0]
                    bestTwo[0] = evaluatedCitizen
                elif curEval > bestTwo[1][0]:
                    bestTwo[1] = evaluatedCitizen
                evalutedGeneration.append(evaluatedCitizen)
            self.currentGeneration = [self.breed(citizen,random.choice(bestTwo)) for citizen in self.currentGeneration[:]]

    def breed(self,aParent,bParentwValue):
        bParent = bParentwValue[1]

        return [((aParent[i]+bParent[i])/2 + random.randint(-self.randomness,self.randomness)) for i in range(len(aParent))] #averages the two parents and then adds randomness

    def __str__(self):
        best = [self.evaluate(self.currentGeneration[0]),self.currentGeneration[0]]
        for i in self.currentGeneration:
            if self.evaluate(i)>best[0]:
                best = [self.evaluate(i),i]
        return str(best[1])


if __name__ == "__main__":
    #just some test code
    def evaluater(x):
        return x[0]-(x[1]**2)
    thing = Species(evaluater,[50,50],100,2)
    thing.evolve(2)
    print thing
