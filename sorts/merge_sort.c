// ================================================
// MERGE SORT - C Program
// ================================================
#include <stdio.h>

// Do sorted parts ko merge karo
void merge(int a[], int left, int mid, int right)
{
    int b[20];
    int i = left, j = mid + 1, k = left;

    while (i <= mid && j <= right)
    {
        if (a[i] <= a[j])
            b[k++] = a[i++];
        else
            b[k++] = a[j++];
    }

    while (i <= mid)
        b[k++] = a[i++];

    while (j <= right)
        b[k++] = a[j++];

    for (i = left; i <= right; i++)
        a[i] = b[i];
}

// Merge sort function
void mergeSort(int a[], int left, int right)
{
    int mid;

    if (left < right)
    {
        mid = (left + right) / 2;
        mergeSort(a, left, mid);
        mergeSort(a, mid + 1, right);
        merge(a, left, mid, right);
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

    mergeSort(a, 0, n - 1);

    printf("Sorted array: ");
    for (i = 0; i < n; i++)
        printf("%d ", a[i]);

    return 0;
}
