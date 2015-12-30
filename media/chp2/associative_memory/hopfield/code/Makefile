all: hopfield

hopfield: hopfield.cpp
	g++ -o hopfield hopfield.cpp --std=c++0x `pkg-config opencv --cflags --libs` -Wall -O3

clean:
	rm -f hopfield
	rm -f *~
	rm -f out/*

