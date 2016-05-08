#Izzulmakin 2016-05-08

EXE = makinplayer

CFLAGS   = --enable-stdcall-fixup
#~ DEFINE = -DWINDOWS
#bellow is the dll path and name
LDFLAGS  = -L./lib/
INCLUDE = -lAutoItX3

CFILES   = $(shell find src -maxdepth 1 -type f -name '*.c')
COBJECTS = $(CFILES:.c=.o)

SOURCES = $(CFILES)
OBJECTS = $(COBJECTS)

CC = gcc


all: $(EXE)
	# Mbuh pie dadine kui mau wkwkwk

$(EXE): $(OBJECTS)
	# Linking...
	$(CC) $(CFLAGS) $(OBJECTS)  $(INCLUDE)  $(LDFLAGS) -o $(EXE)

src/%.o: src/%.c
	# Compiling $<...
	$(CC) $< -c $(INCLUDE)  $(LDFLAGS) -o $@

run: all
	./$(EXE)

clean:
	# Cleaning...
	rm -f $(EXE) $(OBJECTS)

