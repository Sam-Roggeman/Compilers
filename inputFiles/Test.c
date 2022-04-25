#include <stdio.h>

int main() {
    int a = 2;
    int *b = &a;
    printf(*b);
    return 1;
}