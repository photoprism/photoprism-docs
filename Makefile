.PHONY: all deps fix pip build serve install install-venv upgrade upgrade-venv replace replace-venv reinstall watch deploy;

UID := $(shell id -u)
GID := $(shell id -g)

export VIRTUAL_ENV := $(abspath "./venv")
export VIRTUAL_ENV_BIN := $(abspath "./venv/bin")
export PATH := $(VIRTUAL_ENV_BIN):$(PATH)

-include .env
export

all: deploy
deps: pip upgrade
install: venv install-venv
upgrade: venv upgrade-venv
replace: venv replace-venv
watch: serve
fix:
	sudo chown -R $(UID):$(GID) .
	sudo chmod -R a+rwX .
pip:
	sudo apt install pip
venv:
	python3 -m venv venv
	. ./venv/bin/activate
upgrade-venv:
	python3 -m venv venv
ifdef GH_TOKEN
	@echo "Found GH_TOKEN, upgrading mkdocs-material-insiders"
	pip3 install --disable-pip-version-check -U git+https://${GH_TOKEN}@github.com/photoprism/mkdocs-material-insiders.git
else
	@echo "GH_TOKEN not set in .env file, upgrading regular mkdocs-material"
	pip3 install --disable-pip-version-check -U mkdocs-material
endif
	pip3 install --disable-pip-version-check -U -r requirements.txt
install-venv:
	python3 -m venv venv
	. ./venv/bin/activate
ifdef GH_TOKEN
	@echo "Found GH_TOKEN, installing mkdocs-material-insiders"
	pip3 install --disable-pip-version-check git+https://${GH_TOKEN}@github.com/photoprism/mkdocs-material-insiders.git
else
	@echo "GH_TOKEN not set in .env file, installing regular mkdocs-material"
	pip3 install --disable-pip-version-check mkdocs-material
endif
	pip3 install --disable-pip-version-check -r requirements.txt
replace-venv:
	pip3 install --disable-pip-version-check -U --force-reinstall  -r requirements.txt
serve:
	mkdocs serve -a 0.0.0.0:8000
build:
	mkdocs build --config-file mkdocs.deploy.yml
deploy:
	mkdocs gh-deploy --force --config-file mkdocs.deploy.yml
pull:
	git checkout master
	git pull origin master
push:
	git checkout master
	git push origin master
merge:
	git checkout deploy
	git pull origin deploy
	git merge master
	git push origin deploy
	git checkout master
