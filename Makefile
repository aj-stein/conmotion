SHELL:=/usr/bin/env bash
NETFLIFY_EXE := node_modules/.bin/netlify
MERMAID_EXE_WRAPPER :=
MERMAID_EXE := node_modules/.bin/mmdc
SITE_SRC_DIR := docs
SITE_BUILD_DIR := build
DIAGRAM_IN_FILES := $(wildcard $(SITE_SRC_DIR)/*.mmd)
DIAGRAM_OUT_FILES := $(patsubst $(SITE_SRC_DIR)/%.mmd, $(SITE_BUILD_DIR)/%.png, $(DIAGRAM_IN_FILES))
OCSF_IN_FILES := $(wildcard $(SITE_SRC_DIR)/*.json)
OCSF_OUT_FILES := $(patsubst $(SITE_SRC_DIR)/%.json, $(SITE_BUILD_DIR)/%.json, $(OCSF_IN_FILES))
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

$(SITE_BUILD_DIR)/%.pdf: $(SITE_SRC_DIR)/%.md $(REFS_FILE)
	mkdir -p $(SITE_BUILD_DIR)
	pandoc $< -o $@ \
		-M colorlinks \
		--resource-path $(SITE_BUILD_DIR) \
		--bibliography $(REFS_FILE) \
		--citeproc \
		--csl $(CITATION_STYLE)

$(SITE_BUILD_DIR)/%.json: $(SITE_SRC_DIR)/%.json
	cp $< $@

$(SITE_BUILD_DIR)/%.html: $(SITE_SRC_DIR)/%.md $(DIAGRAM_OUT_FILES) $(OCSF_OUT_FILES) $(REFS_FILE)
	pandoc $< -o $@ \
		--resource-path $(SITE_BUILD_DIR) \
		--bibliography $(REFS_FILE) \
		--citeproc \
		--csl $(CITATION_STYLE)

$(SITE_BUILD_DIR)/%.png: $(SITE_SRC_DIR)/%.mmd $(MERMAID_EXE)
	mkdir -p $(SITE_BUILD_DIR)
	# Explanation: 
	# https://github.com/mermaid-js/mermaid-cli/issues/730#issuecomment-2408615110
	$(MERMAID_EXE_WRAPPER) \
		npx -p @mermaid-js/mermaid-cli \
			mmdc -i $< -o $@ -b transparent --scale 2

tag:
	sed -i'' "s|/develop|$(shell git rev-parse HEAD)|g" $(SITE_SRC_DIR)/architecture.md

render: $(DIAGRAM_OUT_FILES)

publish: $(WEBPAGE_OUT_FILES) $(OCSF_OUT_FILES)

convert: $(SITE_BUILD_DIR)/architecture.pdf

clean:
	rm -rf $(SITE_BUILD_DIR)


.PHONY: clean dependencies tag render publish convert all

all: clean dependencies tag render publish convert
