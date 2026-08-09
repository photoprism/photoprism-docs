.PHONY: all deps fix pip build serve install replace upgrade venv install-venv upgrade-venv replace replace-venv reinstall watch deploy spellcheck install-typos vale install-vale check-links check-links-external install-muffet muffet format-whitespace format-whitespace-check format-tables;

UID := $(shell id -u)
MUFFET_PORT ?= 8042
MUFFET_ARGS ?=
GID := $(shell id -g)

export VIRTUAL_ENV := $(abspath "./venv")
export VIRTUAL_ENV_BIN := $(abspath "./venv/bin")
export PATH := $(VIRTUAL_ENV_BIN):$(PATH)

-include .env
export

all: deploy
deps: pip upgrade
install: install-venv
upgrade: remove-venv install-venv
replace: upgrade
watch: serve
fix:
	sudo chown -R $(UID):$(GID) .
	sudo chmod -R a+rwX .
pip:
	# Use python3-full (a metapackage that depends on the active python3.X-venv
	# / python3.X-dev) instead of bare python3-venv. On Ubuntu 26.04 / Debian
	# trixie+, python3-venv is a transitional package that no longer reliably
	# pulls in the version-specific ensurepip/venv module needed for
	# `python3 -m venv`, so install-venv fails with "ensurepip is not available".
	sudo apt-get install -y git python3-full python3-pip python3-wheel
venv: install-venv
remove-venv:
	rm -rf ./venv
install-venv:
	python3 -m venv venv
	. ./venv/bin/activate
	./venv/bin/pip3 install wheel
	# Material for MkDocs Insiders is now free for everyone:
    # https://squidfunk.github.io/mkdocs-material/blog/2025/11/11/insiders-now-free-for-everyone/#switching-from-insiders
	./venv/bin/pip3 install --disable-pip-version-check mkdocs-material
	./venv/bin/pip3 install --disable-pip-version-check -r requirements.txt
serve:
	./venv/bin/properdocs serve --watch docs --watch overrides --watch mkdocs.yml -a 0.0.0.0:8000
build:
	./venv/bin/properdocs build --config-file mkdocs.deploy.yml
deploy:
	./venv/bin/properdocs gh-deploy --force --config-file mkdocs.deploy.yml
pull:
	git checkout develop
	git pull origin develop
push:
	git checkout develop
	git push origin develop
install-typos:
	./scripts/install-typos.sh
spellcheck: install-typos
	# Report-only spell check of docs/, configured in _typos.toml. To apply the suggested
	# corrections instead of just listing them, run: ./bin/typos --write-changes docs/
	./bin/typos docs/
install-vale:
	./scripts/install-vale.sh
vale: install-vale
	# OPTIONAL, under evaluation: prose-style linting, configured in .vale.ini. Not part of
	# "make build" and not a gate, so a non-zero vale exit status is deliberately swallowed.
	# See the comments in .vale.ini before acting on the output.
	-./bin/vale docs/
check-links:
	# Report internal links and assets in site/ that do not resolve. Needs a build
	# first (make build) and no network; exits non-zero when something is missing.
	node scripts/check-links.js
check-links-external:
	# Also probe external URLs. Advisory only - a third party rate-limiting us is
	# not our build breaking - so a non-zero exit is deliberately swallowed.
	-node scripts/check-links.js --external
install-muffet:
	./scripts/install-muffet.sh
muffet: install-muffet
	# Crawl the built site with muffet, which also validates in-page anchors that
	# check-links does not. Served locally on purpose: crawling the live site would
	# fill its access logs with our own checks. Advisory - muffet judges by status
	# code, so SPA deep links and bot-challenged hosts show up as false positives.
	@test -f site/index.html || { echo "No build found in site/ - run 'make build' first." >&2; exit 1; }
	@cd site && python3 -m http.server $(MUFFET_PORT) --bind 127.0.0.1 >/dev/null 2>&1 & \
	  SRV=$$!; trap 'kill $$SRV 2>/dev/null' EXIT INT TERM; sleep 2; \
	  ./bin/muffet --max-connections 16 --buffer-size 8192 $(MUFFET_ARGS) http://127.0.0.1:$(MUFFET_PORT)/ || true
img-resize:
	mogrify -resize '1000x860>' docs/user-guide/img/*.jpg
	mogrify -resize '1000x860>' docs/user-guide/**/img/*.jpg
	mogrify -resize '1000x860>' docs/getting-started/nas/img/asustor/*.jpg
merge:
	git checkout deploy
	git pull origin deploy
	git merge develop
	git push origin deploy
	git checkout develop
format-whitespace:
	# Normalize blank-line runs, trailing spaces, and the final newline across docs/.
	# Two trailing spaces are a Markdown hard break and are preserved.
	python3 ./scripts/format-whitespace.py
format-whitespace-check:
	# Report the whitespace drift without modifying files; exits non-zero on drift.
	python3 ./scripts/format-whitespace.py --check
format-tables:
	# Reformat Markdown tables. Fenced code blocks are masked so sample CLI
	# output drawn with pipes is not rewritten.
	# The tensorflow table is centre-aligned with no leading pipe: padding pushes it
	# past four leading spaces, which Markdown then reads as an indented code block.
	python3 ./scripts/format-tables.py --exclude docs/developer-guide/vision/tensorflow/index.md
