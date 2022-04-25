#include <stdio.h>

// WORKS

// This should print 1 and 0 alternating 
int main(){
        printf("%d; ", 1 < 2);
        printf("%d; ", 1 > 2);
        printf("%d; ", 1 <= 2);
        printf("%d; ", 1 >= 2);
        printf("%d; ", (0.5f > 0.0f) != (0.0f > 1.0f));
        return 1;
}