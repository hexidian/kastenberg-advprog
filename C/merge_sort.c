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
    if (array[0] > array[1]) {return array}
    int returningArray[2]; returningArray[0] = array[1]; returningArray[1] = array[0]; //just makes an array that is the reverse of the starting array
    return returningArray;
  }
  //TODO split up the array and then combine the sorted version

}
int main ()
{
  srand(time(NULL));
  int ElementRange = 40;
  int startArray[ListLength];
  for (int i = 0; i<ListLength; i++)
  {
    startArray[i] = rand() % 40;
  }
  return 1;
}
