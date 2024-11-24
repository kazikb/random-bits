/*
    Kazimierz Biskup
    https://github.com/kazikb/random-bits
*/
#define _GNU_SOURCE     // contains type ssize_t
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <fcntl.h>      // contains definitions of constants such as: O_CREAT
#include <unistd.h>     // contains POSIX API, i.e. read(), write() definitions
#include <sys/stat.h>   // contains mkdir

#define INIT_LIST_CAPACITY 2
#define WRITE_PERMS_POSSITION 1

/* A structure for storing strings with results */
typedef struct _entryTable {
    char **list;
    size_t count;
    size_t capacity;
} entryTable;

/* A structure containing information about the process collected from a file
 * /proc/pid/maps
 */
typedef struct _procInfo {
    int pid;
    int totalMemory;
    entryTable wRegions;
    entryTable librarys;
} procInfo;

/* A structure containing information about the process for the purpose of
 * dumping to a file.
 */
typedef struct _memRegion {
    unsigned long int addr_start;
    unsigned long int addr_end;
    int size;
    char *perm;
} memRegion;

/* Field names in the file /proc/pid/maps */
typedef enum _mapsFields {
    FIELD_ADDRESS  = 0,
    FIELD_PERMS    = 1,
    FIELD_OFFSET   = 2,
    FIELD_DEV      = 3,
    FIELD_INODE    = 4,
    FIELD_PATHNAME = 5
} mapsFields;

/* File parsing function /proc/pid/maps */
int getProcMapsInfo(procInfo *pProcInfo);

/* A function that parses lines from a file /proc/pid/maps */
int parseMapsLine(procInfo *pProcInfo, char *pLine);

/* Function that displays the contents of the procInfo structure */
void printProcInfo(procInfo *pProcInfo);

/* Function initializing the structure with information about the process */
int initProcInfo(int pid, procInfo *pProcInfo);

/* Function initializing the entryTable structure */
int initEntryTable(entryTable *pEntryTable);

/* A function that adds a string to the array contained in the entryTable
 * structure. If necessary, enlarge the array in the <list> field to accommodate
 * additional elements.
 */
int appendEntryTable(entryTable *pEntryTable, char *pEntry);

/* Function to dump process memory regions to files. A folder with the process
 * PID in its name will be created in the current directory to which memory
 * dumps will be written.
 */
int dumpMemoryRegions(procInfo *pProcInfo);

/* A function whose task is to fill the _memRegion structure with information
 * contained in the /proc/pid/maps file.
 */
int parseMemoryRegionInfo(memRegion *memRegion, char *mapsLine);

/* The actual function that dumps memory regions to a file. */
int dumpMemoryRegionToFile(memRegion *memRegion, char *path, int mem_fd);
