.PHONY: all deps fix pip install upgrade reinstall watch deploy;

UID := $(shell id -u)
GID := $(shell id -g)

-include .env
export

all: deploy
deps: pip upgrade
watch: upgrade serve
fix:
	sudo chown -R $(UID):$(GID) .
	sudo chmod -R a+rwX .
pip:
	sudo apt install pip
upgrade:
	pip3 install --user --no-warn-script-location -U -q -r requirements.txt
install:
ifdef GH_TOKEN
	pip install --user --no-warn-script-location git+https://${GH_TOKEN}@github.com/photoprism/mkdocs-material-insiders
else
	@echo "GH_TOKEN not set in .env file, skipped installing mkdocs-material-insiders"
endif
	pip3 install --user --no-warn-script-location -r requirements.txt
replace:
	pip3 install --user --no-warn-script-location -U --force-reinstall  -r requirements.txt
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
