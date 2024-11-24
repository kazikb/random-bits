/*
    Kazimierz Biskup
    https://github.com/kazikb/random-bits
*/
#include "libmemparser.h"

int getProcMapsInfo(procInfo *pProcInfo)
{
    char *pFilePath = NULL;
    FILE *pFile;
    char *line = NULL;
    size_t lineLen = 0;
    ssize_t getLineSize = 0;

    if (asprintf(&pFilePath, "/proc/%d/maps", pProcInfo->pid) == -1) {
        perror("Failed to build file path variable");
        return 1;
    }

    pFile = fopen(pFilePath, "r");
    if (pFile == NULL) {
        perror("Failed to open maps file for process");
        free(pFilePath);
        return 1;
    }

    while((getLineSize = getline(&line, &lineLen, pFile)) != -1) {
        if (parseMapsLine(pProcInfo, line) != 0) {
            printf("Cannot parse line with address: %s\n", line);
        }
    }

    free(line);
    free(pFilePath);
    if (fclose(pFile) != 0) {
        perror("Failed to close maps file for process");
        return 1;
    }
    return 0;
}

int parseMapsLine(procInfo *pProcInfo, char *pLine)
{
    char *parseLine = strdup(pLine);
    char *token = NULL;
    char *libraryEntry = NULL;
    unsigned long int addrStart = 0ul;
    unsigned long int addrEnd = 0ul;
    mapsFields currentField = FIELD_ADDRESS;
    unsigned short int addLibFlag = 1;

    // Splits the passed string into fields separated by \s
    token = strtok(pLine, " ");
    sscanf(token, "%lx-%lx", &addrStart, &addrEnd);
    pProcInfo->totalMemory = pProcInfo->totalMemory + (addrEnd - addrStart);

    while (token != NULL) {
        // permission section
        if (currentField == FIELD_PERMS) {
            if (appendEntryTable(&pProcInfo->wRegions, parseLine) != 0) {
                free(parseLine);
                return 1;
            }
            parseLine = NULL;
        }

        // library section
        if (currentField == FIELD_PATHNAME) {
            if (token[0] != '[' && token[0] != '\n') {
                for (size_t i = 0; i < pProcInfo->librarys.count; i++) {
                    if (strcmp(token, pProcInfo->librarys.list[i]) == 0) {
                        addLibFlag = 0; // the library is already on the list
                        break;
                    }
                }
            } else {
                addLibFlag = 0;
            }

            if (addLibFlag) {
                libraryEntry = strdup(token);
                if (appendEntryTable(&pProcInfo->librarys, libraryEntry) != 0) {
                    free(libraryEntry);
                    return 1;
                }
            }
        }

        currentField++;
        token = strtok(NULL, " ");
    }

    return 0;
}

void printProcInfo(procInfo *pProcInfo)
{
    char *wPage = NULL;
    char *addrRange = NULL;
    mapsFields currentField = FIELD_ADDRESS;

    printf("Memory sum: %.2lf MB\n\n",
        (pProcInfo->totalMemory / (double)(1024 * 1024))
    );

    printf("Writable pages:\n");
    printf("%-30s%-8s%-10s%s\n",
        "[address]", "[perms]",
        "[offset]", "[pathname]"
    );
    for (size_t i = 0; i < pProcInfo->wRegions.count; i++) {
        wPage = strtok(pProcInfo->wRegions.list[i], " ");

        while (wPage != NULL) {
            if (currentField == FIELD_ADDRESS)
                addrRange = strdup(wPage);
            else if (currentField == FIELD_PERMS) {
                if (wPage[WRITE_PERMS_POSSITION] == 'w') {
                    printf("%-30s", addrRange);
                    printf("%-8s", wPage);
                } else
                    break;
            }
            else if (currentField == FIELD_OFFSET)
                printf("%-10s", wPage);
            else if (currentField == FIELD_PATHNAME)
                printf("%s", wPage);

            currentField++;
            wPage = strtok(NULL, " ");
        }
        currentField = FIELD_ADDRESS;
        free(pProcInfo->wRegions.list[i]);
    }
    free(pProcInfo->wRegions.list);

    printf("\nLibrarys\n");
    for (size_t i = 0; i < pProcInfo->librarys.count; i++) {
        printf("%s", pProcInfo->librarys.list[i]);
        free(pProcInfo->librarys.list[i]);
    }
    free(pProcInfo->librarys.list);
}

int initProcInfo(int pid, procInfo *pProcInfo)
{
    // Initializing the table with memory areas to write to
    if (initEntryTable(&pProcInfo->wRegions) != 0) {
        perror("Failed to allocate memory for wRegions");
        return 1;
    }
    // Initializing the table with the library list
    if (initEntryTable(&pProcInfo->librarys) != 0) {
        perror("Failed to allocate memory for librarys");
        return 1;
    }
    pProcInfo->pid = pid;
    pProcInfo->totalMemory = 0;
    return 0;
}

int initEntryTable(entryTable *pEntryTable)
{
    pEntryTable->list = malloc(INIT_LIST_CAPACITY * sizeof(char *));
    if (pEntryTable->list == NULL) {
        perror("Failed to allocate memory for a table");
        return 1;
    }
    pEntryTable->count = 0;
    pEntryTable->capacity = INIT_LIST_CAPACITY;
    return 0;
}

int appendEntryTable(entryTable *pEntryTable, char *pEntry)
{
    if (pEntryTable->count >= pEntryTable->capacity) {
        pEntryTable->capacity *= 2;
        char **pListTemp = realloc(
            pEntryTable->list,
            pEntryTable->capacity * sizeof(char *)
        );
        if (pListTemp == NULL) {
            perror("Cannot resize table");
            return 1;
        }

        pEntryTable->list = pListTemp;
    }

    pEntryTable->list[pEntryTable->count] = pEntry;
    pEntryTable->count++;
    return 0;
}

int dumpMemoryRegions(procInfo *pProcInfo)
{
    memRegion memRegion;
    struct stat st;
    int mem_fd = 0;
    char *outDir = NULL;
    char *procMemPath = NULL;

    if (asprintf(&outDir, "%d", pProcInfo->pid) == -1) {
        perror("Failed to build output directory path variable");
        return 1;
    }

    if (stat(outDir, &st) != 0) {
        if (mkdir(outDir, 0755) == -1) {
            perror("Cannot create output directory");
            return 1;
        }
    }

    if (asprintf(&procMemPath, "/proc/%d/mem", pProcInfo->pid) == -1) {
        perror("Failed to build process memory file path");
        return 1;
    }

    mem_fd = open(procMemPath, O_RDONLY);
    if (mem_fd == -1) {
        perror("Cannot opend memory file for process");
        return 1;
    }

    for (size_t i = 0; i < pProcInfo->wRegions.count; i++) {
        parseMemoryRegionInfo(&memRegion, pProcInfo->wRegions.list[i]);
        printf("0x%lx-0x%lx %s %d\n", memRegion.addr_start, memRegion.addr_end, memRegion.perm, memRegion.size);

        dumpMemoryRegionToFile(&memRegion, outDir, mem_fd);

        free(pProcInfo->wRegions.list[i]);
    }

    close(mem_fd);
    free(pProcInfo->wRegions.list);
    return 0;
}

int parseMemoryRegionInfo(memRegion *memRegion, char *mapsLine)
{
    char *page = NULL;
    mapsFields currentField = FIELD_ADDRESS;

    page = strtok(mapsLine, " ");
    while (page != NULL) {
        if (currentField == FIELD_ADDRESS)
            sscanf(page, "%lx-%lx", &memRegion->addr_start, &memRegion->addr_end);
        else if (currentField == FIELD_PERMS)
            memRegion->perm = strdup(page);
        else
            break;

        currentField++;
        page = strtok(NULL, " ");
    }
    memRegion->size = memRegion->addr_end - memRegion->addr_start;
    return 0;
}

int dumpMemoryRegionToFile(memRegion *memRegion, char *path, int mem_fd)
{
    int dump_fd = 0;
    char *buffer = (char *)malloc(memRegion->size);
    char *outFile = NULL;
    ssize_t bytes_read = 0;
    ssize_t bytes_write = 0;

    if (asprintf(&outFile, "%s/0x%lx_%d_%s.bin", path, memRegion->addr_start,
            memRegion->size, memRegion->perm) == -1
        ) {
        perror("Failed to build output dump file name");
        return 1;
    }

    dump_fd = open(outFile, O_CREAT | O_WRONLY | O_TRUNC, 0644);
    if (dump_fd == -1) {
        perror("Cannot create dump file");
        return 1;
    }

    // Setting offset to the begining of memory region to dump
    if (lseek(mem_fd, memRegion->addr_start, SEEK_SET) == -1) {
        perror("Cannot move file pointer to offset at memory location");
        close(dump_fd);
        return 1;
    }

    bytes_read = read(mem_fd, buffer, memRegion->size);
    if (bytes_read == -1) {
        perror("Cannot read from process memory");
        close(dump_fd);
        return 1;
    }

    bytes_write = write(dump_fd, buffer, bytes_read);
    if (bytes_write == -1) {
        perror("Cannot write memory dump");
        close(dump_fd);
        return 1;
    }

    close(dump_fd);
    return 0;
}
