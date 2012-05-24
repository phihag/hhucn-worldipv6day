
default: all

all: png pdf

png:
	inkscape --export-png=poster.png poster.svg

pdf:
	inkscape --export-pdf=poster.pdf poster.svg

.PHONY: default all png pdf
