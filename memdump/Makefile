# Define the C compiler to use
CC = gcc

# Define common compiler flags
CFLAGS_COMMON  = -std=c11 -Wall -Wextra
CFLAGS_DEBUG   = $(CFLAGS_COMMON) -g
CFLAGS_RELEASE = $(CFLAGS_COMMON)

# Subdirectories for builds
BUILDDIR   = build
DEBUGDIR   = $(BUILDDIR)/debug
RELEASEDIR = $(BUILDDIR)/release

# Define the name of the executable
PROGRAM_NAME = memparser

# Source files and object files
SRCFILES = main.c libmemparser.c
OBJFILES = $(SRCFILES:.c=.o)

# all of the below is generic - one typically only adjusts the above

# Default target
all: release

# Build debug executable
debug: CFLAGS=$(CFLAGS_DEBUG)
debug: $(DEBUGDIR)/$(PROGRAM_NAME)

# Build release executable
release: CFLAGS=$(CFLAGS_RELEASE) -static
release: $(RELEASEDIR)/$(PROGRAM_NAME)

# Linking for debug
# The entry $(OBJFILES:%=$(DEBUGDIR)/%) corresponds to substitution reference
# foo := a.o b.o l.a c.o
# bar := $(foo:%.o=%.c)
# sets ‘bar’ to ‘a.c b.c l.a c.c’.
# https://www.gnu.org/software/make/manual/make.html#Substitution-Refs
$(DEBUGDIR)/$(PROGRAM_NAME): $(OBJFILES:%=$(DEBUGDIR)/%)
	@mkdir -p $(DEBUGDIR)
	$(CC) $(CFLAGS) -o $@ $^

# Linking for release
$(RELEASEDIR)/$(PROGRAM_NAME): $(OBJFILES:%=$(RELEASEDIR)/%)
	@mkdir -p $(RELEASEDIR)
	$(CC) $(CFLAGS) -o $@ $^

# Compiling source files into object files
# Wyjaśnienie notacji charakterystycznej dla Makefile
# %.o -> odpowiada $@
# %.c -> odpowiada $<
$(DEBUGDIR)/%.o: %.c
	@mkdir -p $(DEBUGDIR)
	$(CC) $(CFLAGS) -c -o $@ $<

$(RELEASEDIR)/%.o: %.c
	@mkdir -p $(RELEASEDIR)
	$(CC) $(CFLAGS) -c -o $@ $<

# Clean generated files
clean:
	rm -rf $(BUILDDIR)
