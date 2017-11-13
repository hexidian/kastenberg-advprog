def find(lookFor,sortedDirectory):
    mini = 0
    maxi = len(sortedDirectory)
    found = False
    while found == False:
        print "one try"
        index = (mini+maxi)/2
        element = sortedDirectory[index][0]
        if element == lookFor:
            found = True
            return sortedDirectory[index]

        if element > lookFor:
            maxi = index

        else:
            mini = index

def main():
    testList = [[1,"person"],[2,"man"],[5,"woman"],[10,"thing"],[23,"not what looking for"]]
    print find(2,testList)

if __name__ == "__main__":
    main()
