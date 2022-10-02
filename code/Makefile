CC = g++
SRC = $(wildcard *.cpp)
BIN = $(SRC:%.cpp=%.out)

all : ${BIN}
 
${BIN}:%.out:%.cpp
	${CC} $^ -o $@ -std=c++11
 
clean:
	rm -rf ${BIN}

.PHONY: all clean