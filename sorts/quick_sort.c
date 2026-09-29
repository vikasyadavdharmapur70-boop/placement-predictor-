// ================================================
// QUICK SORT - C Program
// ================================================
#include <stdio.h>

// Partition function: pivot ke left me chhote, right me bade
int partition(int a[], int low, int high)
{
    int pivot = a[high];
    int i = low - 1;
    int j, temp;

    for (j = low; j < high; j++)
    {
        if (a[j] < pivot)
        {
            i++;
            temp = a[i];
            a[i] = a[j];
            a[j] = temp;
        }
    }
    temp = a[i + 1];
    a[i + 1] = a[high];
    a[high] = temp;

    return i + 1;
}

// Quick sort function
void quickSort(int a[], int low, int high)
{
    int p;

    if (low < high)
    {
        p = partition(a, low, high);
        quickSort(a, low, p - 1);
        quickSort(a, p + 1, high);
    }
}

int main()
{
    int a[20], n, i;

    printf("Enter number of elements: ");
    scanf("%d", &n);

    printf("Enter %d elements: ", n);
    for (i = 0; i < n; i++)
        scanf("%d", &a[i]);

    quickSort(a, 0, n - 1);

    printf("Sorted array: ");
    for (i = 0; i < n; i++)
        printf("%d ", a[i]);

    return 0;
}
