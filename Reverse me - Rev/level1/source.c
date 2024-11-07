#include <stdio.h>
#include <string.h>
#include <stdlib.h>


int main (int argc, char **argv)
{
    char input[1000000];
    printf("Please enter key: ");
    fgets(input, sizeof(input), stdin);
    if (!strcmp("__stack_check", input) == 0)
        printf("Nope.\n");
    else
        printf("Good job.\n");
}