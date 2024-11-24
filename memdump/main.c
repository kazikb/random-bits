/*
    Kazimierz Biskup
    https://github.com/kazikb/random-bits
*/
#include <errno.h>
#include "libmemparser.h"

void printHelp(char *pName);
int getProcInfo(int pid);
int dumpProcMem(int pid);

int main(int argc, char *argv[])
{
    enum cmdArgs {FIELD_FILE, FIELD_MODE, FIELD_PID};
    int returnCode = 0;
    int pid = 0ul;

    if (argc != 3) {
        printHelp(argv[FIELD_FILE]);
        return 1;
    }
    else if ((strcmp(argv[FIELD_MODE], "-i") != 0)
            && (strcmp(argv[FIELD_MODE], "-d") != 0)
        ) {
        printHelp(argv[FIELD_FILE]);
        return 1;
    }

    errno = 0;  /* To distinguish success/failure after call */
    pid = strtol(argv[FIELD_PID], NULL, 10);
    if (errno == ERANGE || errno == EINVAL) {
        perror("PID conversion");
        return 1;
    }

    if (strcmp(argv[FIELD_MODE], "-i") == 0)
        returnCode = getProcInfo(pid);
    else if (strcmp(argv[FIELD_MODE], "-d") == 0)
        returnCode = dumpProcMem(pid);

    return returnCode;
}

void printHelp(char *pName)
{
    printf("Get process information\n");
    printf("\t%s -i [PID]\n", pName);
    printf("Dumping process memory regions\n");
    printf("\t%s -d [PID]\n", pName);
}

int getProcInfo(int pid)
{
    procInfo ProcInfo;

    // Inicjalizacja struktury z informacjami o procesie
    if (initProcInfo(pid, &ProcInfo) != 0) {
        perror("Failed to initialize procInfo");
        return 1;
    }

    if (getProcMapsInfo(&ProcInfo) != 0) {
        return 1;
    }

    printProcInfo(&ProcInfo);
    return 0;
}

int dumpProcMem(int pid)
{
    procInfo ProcInfo;

    if (initProcInfo(pid, &ProcInfo) != 0) {
        perror("Failed to initialize procInfo");
        return 1;
    }

    if (getProcMapsInfo(&ProcInfo) != 0) {
        return 1;
    }

    dumpMemoryRegions(&ProcInfo);
    return 0;
}
