
#include <stdio.h>

// This should print 1 and 0 alternating 
int main(){

        printf("%d; ", 1 && 2);
        printf("%d; ", 0 && 2);
        printf("%d; ", 1 || 2);
        printf("%d; ", 0 || 0);
        printf("%d; ", (0.5f || 0.0f) && (0.0f || 1.0f));
        printf("%d; ", !(1 && 2));
        return 1;
}