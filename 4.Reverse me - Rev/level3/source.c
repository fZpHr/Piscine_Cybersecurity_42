#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

void no() {
    printf("Nope.\n");
    exit(1);
}

void ok() {
    printf("Good job.\n");
    exit(0);
}

int main(int argc, const char **argv, const char **envp) {
    char v3; // al
    size_t v5; // [esp+10h] [ebp-48h]
    bool v6; // [esp+17h] [ebp-41h]
    char nptr[4]; // [esp+1Fh] [ebp-39h] BYREF
    char v8[24]; // [esp+23h] [ebp-35h] BYREF
    char v9[23]; // [esp+24h] [ebp-34h]
    char s[9]; // [esp+3Bh] [ebp-1Dh] BYREF
    size_t v11; // [esp+44h] [ebp-14h]
    int i; // [esp+48h] [ebp-10h]
    int v13; // [esp+4Ch] [ebp-Ch]
    int v14; // [esp+50h] [ebp-8h]

    v14 = 0;
    printf("Please enter key: ");
    v13 = scanf("%23s", v8); // Lire une chaîne de caractères de l'utilisateur
    if (v13 != 1)
        no(); // Si la lecture échoue, appeler la fonction no()
    
    if (v8[0] != '4')
        no(); // Vérifier si le premier caractère est '4', sinon appeler no()
    if (v8[1] != '2')
        no(); // Vérifier si le deuxième caractère est '2', sinon appeler no()
    fflush(stdin); // Vider le buffer d'entrée
    memset(s, 0, sizeof(s)); // Initialiser la chaîne s avec des zéros
    s[0] = '*'; // Mettre '*' comme premier caractère de s
    nptr[3] = 0; // Terminer nptr avec un caractère nul
    v11 = 3; // Initialiser v11 à 3
    for (i = 1;; ++i) {
        v6 = 0;
        if (strlen(s) < 8) { // Vérifier si la longueur de s est inférieure à 8
            v5 = v11;
            v6 = v5 < strlen(v8); // Vérifier si v11 est inférieur à la longueur de v8
        }
        if (!v6)
            break; // Sortir de la boucle si v6 est faux
        nptr[0] = v8[v11 - 1]; // Copier le caractère précédent dans nptr[0] v8[42042042042042042042042]
                                                                //                ^
        nptr[1] = v8[v11]; // Copier le caractère actuel dans nptr[1]       v8[42042042042042042042042]
                                                                //                ^
        nptr[2] = v8[v11 + 1]; // Copier le caractère suivant dans nptr[2]  v8[42042042042042042042042]
                                                                //                 ^
        v3 = atoi(nptr); // Convertir nptr en entier
        s[i] = v3; // Mettre l'entier converti dans s
        v11 += 3; // Incrémenter v11 de 3
    }
    s[i] = 0; // Terminer s avec un caractère nul
    if (strcmp(s,"********"))
        no(); // Comparer s avec "********", si différent appeler no()
    ok(); // Si tout est correct, appeler ok()
    return 0;
}
