#!/bin/bash

./clean.sh

FILES="`find chapters/ appendix/ frontmatter/ backmatter/ -name "*.tex" | sort` glossary.tex"

for FILE in $FILES; do
	echo "============="
	echo $FILE
	echo "============="

	# List uses of "an" and "a" in combination with vowels
	ack -i --color --color-match=on_magenta "($|\\s)(a\\s+[aeiou])" $FILE
	ack -i --color --color-match=on_magenta "($|\\s)(an\\s+[bcdfghklmnpqrstvwu])" $FILE
	ack -i --color --color-match=on_green "($|\\s)(an\\s+[aeiou])" $FILE

	# Uppercase after colon
	ack --color --color-match=on_blue ":\\s+[A-Z]" $FILE

	# British english
	ack -i --color --color-match=on_red '(?!size).iz' $FILE

	# Unwanted word repetition
	ack -i --color --color-match=on_yellow '\b((\w*[aeiou]\w*)(?:\s+\2\b)+)' $FILE

	# Dummy citation
	ack -i --color --color-match="black on_white" '\\cite\{xxx\}' $FILE

	# "." at the end of short figure descriptions
	ack -i --color --color-match="on_blue" '\\(caption|([a-z]*(table|figure)))\s*\[.*(\.)\]' $FILE

	# Denglish phrases
	ack -i --color --color-match=on_red '(in how far|under circumstances|among others|sane|allows? for)' $FILE

	echo
done

