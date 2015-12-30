.PHONY: master_astoecke_design_space_exploration_2015.pdf clean check

all: master_astoecke_design_space_exploration_2015.pdf

master_astoecke_design_space_exploration_2015.pdf:
	latexmk -pdf master_astoecke_design_space_exploration_2015
	if which exiftool ; then exiftool -tagsfromfile metadata.xmp master_astoecke_design_space_exploration_2015.pdf -all:all; fi

clean:
	./clean.sh

check:
	./check.sh

