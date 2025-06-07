SHELL:=/usr/bin/env bash
NETFLIFY_EXE := node_modules/.bin/netlify
MERMAID_EXE := node_modules/.bin/mmdc
SITE_SRC_DIR := docs
SITE_BUILD_DIR := build
DIAGRAM_IN_FILES := $(wildcard $(SITE_SRC_DIR)/*.mmd)
DIAGRAM_OUT_FILES := $(patsubst $(SITE_SRC_DIR)/%.mmd, $(SITE_BUILD_DIR)/%.png, $(DIAGRAM_IN_FILES))
WEBPAGE_IN_FILES := $(wildcard $(SITE_SRC_DIR)/*.md)
WEBPAGE_OUT_FILES := $(patsubst $(SITE_SRC_DIR)/%.md, $(SITE_BUILD_DIR)/%.html, $(WEBPAGE_IN_FILES))
CITATION_STYLE := vendor/csl/apa-6th-edition.csl
REFS_FILE := docs/references.bib

$(CITATION_STYLE):
	git submodule update --init --recursive

$(NETLIFY_EXE):
	npm ci

$(MERMAID_EXE):
	npm ci

dependencies: $(CITATION_STYLE) $(NETLIFY_EXE) $(MERMAID_EXE)

$(SITE_BUILD_DIR)/%.html: $(SITE_SRC_DIR)/%.md $(DIAGRAM_OUT_FILES) $(REFS_FILE)
	pandoc $< -o $@ \
		--bibliography $(REFS_FILE) \
		--citeproc \
		--csl $(CITATION_STYLE)

$(SITE_BUILD_DIR)/%.png: $(SITE_SRC_DIR)/%.mmd $(MERMAID_EXE)
	mkdir -p $(SITE_BUILD_DIR)
	npx -p @mermaid-js/mermaid-cli \
		mmdc -i $< -o $@

tag:
	sed -i'' "s|/develop|$(shell git rev-parse HEAD)|g" $(SITE_SRC_DIR)/architecture.md

publish: $(WEBPAGE_OUT_FILES) $(DIAGRAM_OUT_FILES)

clean:
	rm -rf $(SITE_BUILD_DIR)

debug:
	@echo $(WEBPAGE_OUT_FILES)

.PHONY: all clean publish

all: clean dependencies tag publish
