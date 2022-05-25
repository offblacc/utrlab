#include <stdio.h>
#include <stdlib.h>

#define MAX_IN 201

void S();
void A();
void B();
void C();

int pos = 0, len = 0;
char arr[MAX_IN] = {'\0'};

// ------------- main --------------
int main() {
    if (!fgets(arr, MAX_IN, stdin)) {
        printf("Input reading error\n");
        return 1;
    }

    while (arr[len] != '\0' && arr[len] != '\n')
        len++;

    if (arr[len] == '\n')
        arr[len] = '\0';

    S();
    printf(arr[pos] == '\0' ? "\nDA\n" : "\nNE\n");
    return 0;
}

// ---------- productions ----------
void S() {
    printf("S");
    switch (arr[pos]) {
        case 'a':
            pos++;
            A();
            B();
            break;
        case 'b':
            pos++;
            B();
            A();
            break;
        default:
            printf("\nNE\n");
            exit(0);
    }
    return;
}

void A() {
    printf("A");
    if (pos < len) {
        switch (arr[pos]) {
            case 'a':
                pos++;
                break;
            case 'b':
                pos++;
                C();
                break;
            default:
                printf("\nNE\n");
                exit(0);
        }
    } else {
        printf("\nNE\n");
        exit(0);
    }
    return;
}

void B() {
    printf("B");
    if (pos + 1 < len) {
        if (arr[pos] == 'c' && arr[pos + 1] == 'c') {
            pos = pos + 2;
            S();
        }
        if (arr[pos] == 'b' && arr[pos + 1] == 'c') {
            pos = pos + 2;
        }
    }
    return;
}

void C() {
    printf("C");
    A();
    A();
    return;
}