#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#define True 1
#define False 0
#define ListLength 20
void PrintSimpleArray(int array[ListLength])
{
  int length = ListLength;
  for (int i = 0; i<length; i++)
  {
    printf("%d , ",array[i]);
  }
  printf("\n");//this allows us to have all of the array elements on one line
  return;
}
int merge_sort(int array[],int arrayLength)
{
  if (arrayLength == 1)
  {
    return array;
  }
  if (arrayLength == 2)
  {
    if (array[0] > array[1]) {return array;}
    int returningArray[2]; returningArray[0] = array[1]; returningArray[1] = array[0]; //just makes an array that is the reverse of the starting array
    return returningArray;
  }

  int aLength = arrayLength/2;
  int bLength = arrayLength - aLength;
  //now I will create two arrays with each of the halves of the main array
  int arrayA[aLength];
  int arrayB[bLength];
  for (int i = 0; i < aLength; i++)
  {
    arrayA[i] = array[i];
  }
  for (int i = aLength; i < arrayLength; i++)//this goes from the end of arrayA to the end of the main array
  {
    arrayB[i] = array[i];
  }

  return join(arrayA,aLength,arrayB,bLength);

}

int join(int arrayA[],int aLength,int arrayB[],int bLength)
{
  int array[aLength+bLength];
  int uptoA = 0; int uptoB = 0;//the upto variables are used as the index we have reached
  while ((uptoA < aLength) && (uptoB < bLength))
  {
    if (arrayA[uptoA] < arrayB[uptoB])
    {
      array[uptoA+uptoB] = arrayA[uptoA];
      uptoA++;
    } else {
      array[uptoA+uptoB] = arrayB[uptoB];
      uptoB++;
    }//else
  }//while
  if (uptoA!=aLength)//if A is the array with remaining elements to be added
  {
    for (int i = uptoA+uptoB; i < aLength+bLength; i++)
    {
      array[i] = arrayA[uptoA];
      uptoA++;
    }
  } else {//if B is the array with elements to be added
    for (int i = uptoB+uptoA; i < aLength+bLength; i++)
    {
      array[i] = arrayB[uptoB];
      uptoB++;
    }//for
  }//else
  return array;
}//int join
int main ()
{
  srand(time(NULL));
  int ElementRange = 40;
  int startArray[ListLength];
  for (int i = 0; i<ListLength; i++)
  {
    startArray[i] = rand() % 40;
  }
  PrintSimpleArray(merge_sort(startArray,ListLength));
  return 1;
}
