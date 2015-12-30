#!/bin/bash
# adapted from Arnaud Ramey (arnaud.a.ramey@gmail.com)
if [ $# -ne 2 ]
then
	echo "Usage: $0 [SVGFILE] [LAYERGROUPS]"
	echo "Example: $0 drawing.svg bg+l1,bg+l2,bg+l3,bg+l4"
	exit 1
fi

INSVGORIG=$1
LAYERGROUPS=$2
TMPFILEPREFIX=`mktemp /tmp/export_layers_XXXXX`
RESULTPREFIX=out/`basename "$INSVGORIG" .svg`

mkdir -p out
rm -rf "$RESULTPREFIX"*

# Remove temporary files
INSVG=$TMPFILEPREFIX.svg
rm -rf "$TMPFILEPREFIX"*

# make all layers invisible
cp "$INSVGORIG" "$INSVG"
xmlstarlet edit --inplace --update "//*[@inkscape:groupmode=\"layer\"]/@style" --value "display:none" "$INSVG" || exit 1

set_layer_visible() {
	# https://stackoverflow.com/questions/7837879/xmlstarlet-update-an-attribute
	xmlstarlet edit --inplace --update "//*[@inkscape:label=\"$2\"]/@style" \
		--value "display:inline" "$1"
}

# for all userlayers
FRAMEIDX=0
IFS=','; for CURRENTLAYERGROUP in $LAYERGROUPS; do
	echo "Processing frame $FRAMEIDX with layers $CURRENTLAYERGROUP"

	CURRENTSVG=${TMPFILEPREFIX}_$FRAMEIDX.svg
	CURRENTOUTPDF=${RESULTPREFIX}_`printf "%03d" $FRAMEIDX`.pdf
	CURRENTOUTPDFCROPPED=${RESULTPREFIX}_`printf "%03d" $FRAMEIDX`_cropped.pdf
	CURRENTOUTPNG=${RESULTPREFIX}_`printf "%03d" $FRAMEIDX`.png

	# make a copy of INSVG for current frame
	cp "$INSVG" "$CURRENTSVG"

	# for all layers in CURRENTLAYERSGROUP
	IFS='+'; for LAYERID in $CURRENTLAYERGROUP; do
		set_layer_visible $CURRENTSVG $LAYERID
	done

	# export both the cropped and the uncropped version
	echo "Export PDF $CURRENTOUTPDF"
	inkscape --export-area-page --without-gui \
		--export-pdf="$CURRENTOUTPDF" "$CURRENTSVG" >> /dev/null
	echo "Export PDF (Cropped) $CURRENTOUTPDFCROPPED"
	inkscape --export-area-drawing --without-gui \
		--export-pdf="$CURRENTOUTPDFCROPPED" "$CURRENTSVG" >> /dev/null
	echo "Export PNG $CURRENTOUTPNG"
	inkscape --export-area-page --without-gui --export-dpi=600 \
		--export-png="$CURRENTOUTPNG" "$CURRENTSVG" >> /dev/null

	# increment frame idx
	FRAMEIDX=$(( $FRAMEIDX + 1 ))
done

