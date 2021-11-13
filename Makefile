.PHONY: all pull watch deploy chown;

UID := $(shell id -u)
GID := $(shell id -g)

all: pull deploy chown
pull:
	docker pull photoprism/mkdocs-material:7
watch:
	docker run --rm -it -p 8000:8000 -v ${PWD}:/docs photoprism/mkdocs-material:7
chown:
	sudo chown -R $(UID):$(GID) .
deploy:
	docker run --rm -it -v ~/.ssh:/root/.ssh -v ${PWD}:/docs photoprism/mkdocs-material:7 gh-deploy
