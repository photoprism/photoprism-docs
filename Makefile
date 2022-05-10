.PHONY: all deps fix pip install upgrade reinstall watch deploy;

UID := $(shell id -u)
GID := $(shell id -g)

all: fix upgrade deploy
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
	pip3 install --user --no-warn-script-location -r requirements.txt
replace:
	pip3 install --user --no-warn-script-location -U --force-reinstall  -r requirements.txt
serve:
	mkdocs serve -a 0.0.0.0:8000
deploy:
	mkdocs gh-deploy --force
