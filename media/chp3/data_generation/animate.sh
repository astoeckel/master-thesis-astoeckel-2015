#!/bin/bash

NNODES=30
LAYERS=frame_0+node_0
for I in `seq 1 $NNODES`; do
	GROUP=frame_$I+node_0
	for J in `seq 1 $I`; do
		GROUP="$GROUP+node_$J"
	done
	LAYERS="$LAYERS,$GROUP"
done
./export_layers_batch.sh algorithm.svg $LAYERS
