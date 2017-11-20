import random      #just for testing the program
import time
def mSort(bigList):
    bigLength = len(bigList)
    if bigLength == 1:
        return bigList
    aList = [bigList[i] for i in range(0,bigLength/2)]
    bList = [bigList[i] for i in range(bigLength/2,bigLength)]

    aList = mSort(aList)
    bList = mSort(bList)


    return merge(aList,bList)

def merge(aList,bList):
    output = []

    while (len(aList)>0) and (len(bList)>0):
        a = minID(aList)
        b = minID(bList)

        if a[0] < b[0]:
            output.append(a)
            aList.remove(a)
        else:
            output.append(b)
            bList.remove(b)


    if len(aList) == 0:
        output.extend(bList)
    else:
        output.extend(aList)
    return output

def minID(listOfLists):
    mini = listOfLists[0]
    for i in listOfLists:
        if i[0] < mini[0]:
            mini = i

    return mini

def maxID(listOfLists):
    mini = listOfLists[0]
    for i in listOfLists:
        if i[0] > mini[0]:
            mini = i

    return mini

def main():
    slist = []#my starting list
    numb_range = input("the elements will be from 0 to what number?")
    for i in range(input("how many elements should be in the list?")):
        slist.append([random.randint(0,numb_range),"just a word for testing"])
    #now the list is ready
    start_time = time.time()
    result = mSort(slist)
    speed = time.time() - start_time
    print "I sorted it in",speed,"seconds.\nthe result is being exported:\n",#result
    #the result is commented out because it takes forever to print
    export = open('output.txt','w')
    export.write(str(result))
    export.close()

if __name__ == "__main__": main()
