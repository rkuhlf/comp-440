# Use standard gcc
CC = gcc

# 1. Get Homebrew Tcl/Tk prefix dynamically
#    (Fallback to standard path if brew command fails)
TCLTK_PREFIX := /usr/local/opt/tcl-tk

# 2. Compiler Flags
#    -I includes the Tcl headers
#    -Wno-deprecated-declarations suppresses warnings about old Tcl APIs that still work
#    -Wno-pointer-sign allows char* vs signed char* (common in old code)
CFLAGS = -g -Wall -Wno-pointer-sign -Wno-deprecated-declarations \
         -I$(TCLTK_PREFIX)/include

# 3. Linker Flags
#    -L points to the library folder
#    -ltcl9.0 -ltk9.0 links specifically against Tcl/Tk 9
#    -rpath ensures the executable finds the dylibs at runtime
LIBS = -L$(TCLTK_PREFIX)/lib -ltcl9tk9.0 -ltcl9.0 -lm
LDFLAGS = -Wl,-rpath,$(TCLTK_PREFIX)/lib

# 4. Source & Object files
EXE = myWish
OBJS = tkAppInit.o PacWarGuts.o PacWarTk.o
SIM_AUX = PacWar.tcl

# Build Rules
all: $(EXE)

$(EXE): $(OBJS)
	$(CC) $(CFLAGS) $(LDFLAGS) $(OBJS) $(LIBS) -o $(EXE)

.c.o:
	$(CC) -c $(CFLAGS) $<

clean:
	rm -rf $(EXE) $(OBJS)

check: myWish $(SIM_AUX)
