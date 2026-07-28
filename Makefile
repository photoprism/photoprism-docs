.PHONY: all deps fix pip build serve install replace upgrade venv install-venv upgrade-venv replace replace-venv reinstall watch deploy spellcheck install-typos vale install-vale;

UID := $(shell id -u)
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
