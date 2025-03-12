#ifndef UTILITIES_H
#define UTILITIES_H

// Include necessary headers
#include <unistd.h>
#include <stdio.h>
#include <errno.h>
#include <sys/stat.h>
#include <dirent.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <limits.h>
#include <libgen.h> 
#include <unistd.h> 




// Return codes
#define SUCCESS 0
#define FAILURE 1

// Argument count constant
#define MAX_ARG_COUNT 2
#define MIN_ARG_COUNT 1
// Argument position for the path
#define PATH_ARG_INDEX 1
#define PROGRAM_NAME_INDEX 0
#define BUFFER_SIZE 1024
#define PATH_SIZE 1024
#define COMMAND_SIZE 1000
#define TICKET_SIZE 256
#define TIMESTAMP_SIZE 64

// Function declaration
int isValidPath(const char *path);
const char *getFileType(mode_t mode);
void formatTimestamp(time_t rawTime, char *buffer, size_t bufferSize);
void createReadableTicket(const char *path, const struct stat *fileStat, char *ticket, size_t ticketSize) ;
char *processPath(const char *path) ;

#endif // UTILITIES_H
