#!/bin/sh

find \( -name "*.run.xml" \
        -o -name "*.acn" \
        -o -name "*.pyg" \
        -o -name "*.xmpi" \
        -o -name "*.acr" \
        -o -name "*.alg" \
        -o -name "*.glo" \
        -o -name "*.loa" \
        -o -name "*.ist" \
        -o -name "*.bbl" \
        -o -name "*.blg" \
        -o -name "*.bcf" \
        -o -name "*.aux" \
        -o -name "*.snm" \
        -o -name "*.out" \
        -o -name "*.toc" \
        -o -name "*.nav" \
        -o -name "*.log" \
        -o -name "*.glg" \
        -o -name "*.gls" \
        -o -name "*.fdb_latexmk" \
        -o -name "*.fls" \
        -o -name "*.backup" \
        -o -name "*~" \) \
        -print \
        -delete

latexmk -C master_astoecke_design_space_exploration_2015
