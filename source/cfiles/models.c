#include "headers/utilities.h"
#include "headers/messages.h"


int main() {
    FILE *fp;
    char buffer[BUFFER_SIZE];
    // Open a process using popen and execute the OLLAMA_LIST command
    fp = popen(OLLAMA_LIST, READ);
    if (fp == NULL) {
        perror(POPEN_FAIL);
        return FAILURE;
    }

    int c = ZERO;
    // Read the output from the process line by line
    while (fgets(buffer, BUFFER_SIZE, fp) != NULL) {
        if (c == ZERO){
            c++;
            continue;
        }
         // Tokenize the buffer using the CURLY delimiter
        char *token = strtok(buffer, CURLY);
        while (token != NULL) {
            printf("%s", token);
            token = strtok(NULL, SPACE);
            break;
        }
    }
    // Close the process and check for errors
    if (pclose(fp) == -ONE) {
        perror(PCLOSE_FAIL);
        return FAILURE;
    }

    return SUCCESS;
}
