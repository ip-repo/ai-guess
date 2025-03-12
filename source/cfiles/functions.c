#include "headers/utilities.h"
#include "headers/messages.h"

// Function to check if a given file path is valid and accessible
int isValidPath(const char *path) {
    // Check if the file or directory exists using access() with F_OK
    if (access(path, F_OK) == SUCCESS) { 
        return SUCCESS; 
    } else {
        // Print an error message if the path is invalid or inaccessible
        perror(ERROR_MESSAGE); 
        return FAILURE; 
    }
}

// Function to determine the type of a file based on its mode
const char *getFileType(mode_t mode) {
    // Use a switch statement to match the file type based on the mode
    switch (mode & S_IFMT) { // Mask the mode with S_IFMT to extract the file type
        // File is a block device
        case S_IFBLK:  return "Block-Device";
        // File is a character device
        case S_IFCHR:  return "Character-Device";
        // File is a directory
        case S_IFDIR:  return "Directory";
        // File is a FIFO (named pipe)
        case S_IFIFO:  return "FIFO/PIPE";
        // File is a regular file
        case S_IFREG:  return "Regular-File";
        // File type is unknown
        default:       return "Unknown";
    }
}

// Function to format a given raw time into a human-readable timestamp
void formatTimestamp(time_t rawTime, char *buffer, size_t bufferSize) {
    // Convert the raw time (time_t) to a tm structure in local time
    struct tm *timeInfo = localtime(&rawTime);
    // Format the time into a string representation (YYYY-MM-DD|HH:MM:SS)
    // and store it in the provided buffer
    strftime(buffer, bufferSize, "%Y-%m-%d|%H:%M:%S", timeInfo);
}


// Function to create a formatted ticket containing file metadata in a readable format
void createReadableTicket(const char *path, const struct stat *fileStat, char *ticket, size_t ticketSize) {
    char formattedTime[TIMESTAMP_SIZE]; // Buffer to hold the formatted timestamp
    const char *fileType = getFileType(fileStat->st_mode); // Get the file type as a string
    formatTimestamp(fileStat->st_mtime, formattedTime, sizeof(formattedTime)); // Format the last modified time of the file

    // Construct the ticket string with metadata: path, file type, size, mode, and formatted time
    snprintf(ticket, ticketSize, "|%s|%s|%ld|%o|%s|",
             path,               // File path
             fileType,           // Type of file (e.g., directory, regular file)
             fileStat->st_size,  // Size of the file in bytes
             fileStat->st_mode,  // Permissions/mode of the file in octal
             formattedTime);     // Last modified time as a formatted string
}




// Function to process a given file path and generate a readable ticket with file metadata
char *processPath(const char *path) {
    struct stat fileStat; // Struct to hold file information
    char *ticket = (char *)malloc(TICKET_SIZE); // Allocate memory for the ticket string

    // Check if memory allocation failed
    if (ticket == NULL) {
        perror(MEM_ERROR); // Print memory error message
        return NULL;       // Return NULL if memory allocation fails
    }

    // Use stat() to get file information; returns 0 on success
    if (stat(path, &fileStat) == ZERO) {
        // Create a readable ticket with metadata if stat() is successful
        createReadableTicket(path, &fileStat, ticket, TICKET_SIZE);
        return ticket; // Return the generated ticket
    } else {
        // Print error message if the path is invalid or inaccessible
        perror(PATH_ERROR);
        free(ticket);  // Free allocated memory before returning
        return NULL;   // Return NULL to indicate failure
    }
}


