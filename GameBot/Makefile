#Izzulmakin 2016-05-08

EXE = makinplayer

CFLAGS   = --enable-stdcall-fixup

#bellow is the dll path and name
LDFLAGS  = -L./lib/new/
INCLUDE = -lAutoItX3 -mwindows

#bellow is the source folder
SRC_MAIN = src_main


CFILES   = $(shell find $(SRC_MAIN) -maxdepth 1 -type f -name '*.c')
COBJECTS = $(CFILES:.c=.o)

SOURCES = $(CFILES)
OBJECTS = $(COBJECTS)

CC = gcc


all: $(EXE)
	# Mbuh pie dadine kui mau wkwkwk

$(EXE): $(OBJECTS)
	# Linking...
	$(CC) $(CFLAGS) $(OBJECTS)  $(INCLUDE)  $(LDFLAGS) -o $(EXE)

$(SRC_MAIN)/%.o: $(SRC_MAIN)/%.c
	# Compiling $<...
	$(CC) $< -c $(INCLUDE)  $(LDFLAGS) -o $@

run: all
	./$(EXE)

clean:
	# Cleaning...
	rm -f $(EXE) $(OBJECTS)

