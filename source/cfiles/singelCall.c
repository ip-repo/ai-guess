#include "functions.c"
#include "headers/utilities.h"
#include "headers/messages.h"

int main(int argc, char *argv[]) {
    // Variable to store the installation path
    char *installPath = "";
    // Buffer to store the file path
    char path[PATH_SIZE];

    // Check if no arguments are passed
    if (argc == ONE) {
         // Get the current working directory and store it in `path`
        if (getcwd(path, sizeof(path)) == NULL) {
            perror(CWD_ERROR);
            return FAILURE;
        }
    } else {
        // Use the first argument as the path
        snprintf(path, sizeof(path), "%s", argv[ONE]);
    }
    // Process the path and create a ticket with metadata
    char *ticket = processPath(path);

    // Check if the ticket creation failed
    if (ticket == NULL) {
        printf(TICKET_ERROR, path);
        return FAILURE;
    } 
    // Buffer to store the command string
    char command[COMMAND_SIZE];

    // Buffer to store the modified ticket
    char newTicket[TICKET_SIZE];

    // Append the installation path to the ticket and store it in `newTicket`
    snprintf(newTicket, sizeof(newTicket) , "%s%s|",ticket,installPath);

    // Construct the command to be executed, including the installation path and ticket
    snprintf(command, sizeof(command), "%s \"%s\"",installPath, newTicket);

    // Free the allocated memory for the ticket
    free(ticket);
    // Execute the constructed command using the system function
    int result = system(command);
    
    return SUCCESS;
}
