.PHONY: all deps fix pip build serve install replace upgrade venv install-venv upgrade upgrade-venv replace replace-venv reinstall watch deploy;

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
	sudo apt-get install -y git python3 python3-pip python3-venv python3-wheel
venv: install-venv
remove-venv:
	rm -rf ./venv
install-venv:
	python3 -m venv venv
	. ./venv/bin/activate
	./venv/bin/pip3 install wheel
ifdef GH_TOKEN
	@echo "Found GH_TOKEN, installing mkdocs-material-insiders"
	./venv/bin/pip3 install --disable-pip-version-check git+https://${GH_TOKEN}@github.com/photoprism/mkdocs-material-insiders.git
else
	@echo "GH_TOKEN not set in .env file, installing regular mkdocs-material"
	./venv/bin/pip3 install --disable-pip-version-check mkdocs-material
endif
	./venv/bin/pip3 install --disable-pip-version-check -r requirements.txt
serve:
	./venv/bin/mkdocs serve -a 0.0.0.0:8000
build:
	./venv/bin/mkdocs build --config-file mkdocs.deploy.yml
deploy:
	./venv/bin/mkdocs gh-deploy --force --config-file mkdocs.deploy.yml
pull:
	git checkout master
	git pull origin master
push:
	git checkout master
	git push origin master
img-resize:
	mogrify -resize '1000x860>' docs/user-guide/img/*.jpg
	mogrify -resize '1000x860>' docs/user-guide/**/img/*.jpg
	mogrify -resize '1000x860>' docs/getting-started/nas/img/asustor/*.jpg
merge:
	git checkout deploy
	git pull origin deploy
	git merge master
	git push origin deploy
	git checkout master
