.PHONY: all deps fix pip install upgrade reinstall watch deploy;

UID := $(shell id -u)
GID := $(shell id -g)

-include .env
export

all: deploy
deps: pip upgrade
watch: serve
fix:
	sudo chown -R $(UID):$(GID) .
	sudo chmod -R a+rwX .
pip:
	sudo apt install pip
upgrade:
ifdef GH_TOKEN
	@echo "Found GH_TOKEN, upgrading mkdocs-material-insiders"
	pip3 install --user --no-warn-script-location --disable-pip-version-check -U git+https://${GH_TOKEN}@github.com/photoprism/mkdocs-material-insiders.git
else
	@echo "GH_TOKEN not set in .env file, upgrading regular mkdocs-material"
	pip3 install --user --no-warn-script-location --disable-pip-version-check -U mkdocs-material
endif
	pip3 install --user --no-warn-script-location --disable-pip-version-check -U -r requirements.txt
install:
ifdef GH_TOKEN
	@echo "Found GH_TOKEN, installing mkdocs-material-insiders"
	pip3 install --user --no-warn-script-location --disable-pip-version-check git+https://${GH_TOKEN}@github.com/photoprism/mkdocs-material-insiders.git
else
	@echo "GH_TOKEN not set in .env file, installing regular mkdocs-material"
	pip3 install --user --no-warn-script-location --disable-pip-version-check mkdocs-material
endif
	pip3 install --user --no-warn-script-location --disable-pip-version-check -r requirements.txt
replace:
	pip3 install --user --no-warn-script-location --disable-pip-version-check -U --force-reinstall  -r requirements.txt
build:
	mkdocs build
serve:
	mkdocs serve -a 0.0.0.0:8000
deploy:
	mkdocs gh-deploy --force
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
