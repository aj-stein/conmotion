SHELL:=/usr/bin/env bash
CSL_STYLE := vendor/csl/apa-6th-edition.csl
SITE_BUILD_DIR := build

$(CSL_STYLE):
	git submodule update --init --recursive

%.html: %.md
	pandoc $< -o $@ \
		--bibliography docs/references.bib --citeproc \
		--csl $(CSL_STYLE)

build/index.html: docs/architecture.html
	mkdir -p $(SITE_BUILD_DIR)
	cp docs/architecture.html $(SITE_BUILD_DIR)/index.html

tag:
	sed -i'' "s|/develop|/$(shell git rev-parse HEAD)|g" docs/architecture.md

publish: build/index.html

clean:
	rm -f docs/*.html
	rm -rf $(SITE_BUILD_DIR)

.PHONY: all clean publish

all: clean $(CSL_STYLE) publish tag
