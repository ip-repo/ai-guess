#ifndef MESSAGES_H
#define MESSAGES_H

// Error and usage messages
#define CWD_ERROR "getcwd() error"
#define PATH_ERROR "Error processing path"
#define MEM_ERROR "Failed to allocate memory"
#define TICKET_ERROR "Failed to generate a ticket for the path: %s\n"
#define ERROR_MESSAGE "Error"
#define USAGE_MESSAGE YELLOW "Usage: %s <path_to_check>\n" RESET
#define PATH_VALID_MESSAGE GREEN "The path '%s' is valid.\n" RESET
#define PATH_INVALID_MESSAGE RED "The path '%s' is not valid.\n" RESET
#define OLLAMA_LIST "ollama list"
#define READ "r"
#define POPEN_FAIL "popen failed"
#define PCLOSE_FAIL "pclose failed"
#define CURLY "{}"
#define SPACE " "
#define ZERO 0 
#define ONE 1
#endif // MESSAGES_H
