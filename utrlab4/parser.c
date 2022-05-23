#include <stdio.h>
#include <stdlib.h>

#define MAX_IN 201

void S();
void A();
void B();
void C();

int pos = 0, len;
char arr[MAX_IN] = {'\0'};

// ------------- main --------------
int main() {
    fgets(arr, MAX_IN, stdin);

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
    if (arr[pos] == 'a') {
        pos++;
        A();
        B();
    } else if (arr[pos] == 'b') {
        pos++;
        B();
        A();
    } else {
        printf("\nNE\n");
        exit(0);
    }
    return;
}

void A() {
    printf("A");
    if (pos < len) {
        if (arr[pos] == 'b') {
            pos++;
            C();
        } else if (arr[pos] == 'a') {
            pos++;
        } else {
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
    if (pos + 1 < len && arr[pos] == 'c' && arr[pos + 1] == 'c') {
        pos = pos + 2;
        S();
    }
    if (pos + 1 < len && arr[pos] == 'b' && arr[pos + 1] == 'c') {
        pos = pos + 2;
    }
    return;
}

void C() {
    printf("C");
    A();
    A();
    return;
}