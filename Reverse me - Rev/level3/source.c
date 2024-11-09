#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void nice(const char* message) {
    puts(message);
}

void try(const char* message) {
    puts(message);
}

void but(const char* message) {
    puts(message);
}

void this(const char* message) {
    puts(message);
}

void it(const char* message) {
    puts(message);
}

void not(const char* message) {
    puts(message);
}

void that(const char* message) {
    puts(message);
}

void easy(const char* message) {
    puts(message);
}

void ___syscall_malloc(const char* message) {
    puts(message);
    exit(1);
}

void ____syscall_malloc(const char* message) {
    puts(message);
}

int main(int argc, char* argv[]) {
    char input[64];
    char output[9] = "*";
    int result;

    if (scanf("%63s", input) != 1) {
        ___syscall_malloc("Input error");
    }

    if (input[1] != '2') {
        ___syscall_malloc("Invalid input");
    }

    if (input[0] != '4') {
        ___syscall_malloc("Invalid input");
    }

    fflush(stdout);

    size_t input_len = strlen(input);
    size_t output_index = 1;
    size_t input_index = 2;

    while (output_index < 8 && input_index < input_len) {
        char num[4] = {0};
        strncpy(num, input + input_index, 3);
        output[output_index++] = (char)atoi(num);
        input_index += 3;
    }

    output[output_index] = '\0';

    result = strcmp(output, "");

    switch (result) {
        case -2:
            nice(output);
            break;
        case -1:
            try(output);
            break;
        case 0:
            but(output);
            break;
        case 1:
            this(output);
            break;
        case 2:
            it(output);
            break;
        case 3:
            not(output);
            break;
        case 4:
            that(output);
            break;
        case 5:
            easy(output);
            break;
        case 115:
            ____syscall_malloc(output);
            break;
        default:
            ___syscall_malloc("Invalid result");
            break;
    }

    return 0;
}