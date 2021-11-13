.PHONY: all watch deploy chown;

UID := $(shell id -u)
GID := $(shell id -g)

all: deploy chown
watch:
	docker run --rm -it -p 8000:8000 -v ${PWD}:/docs squidfunk/mkdocs-material:7.3.6
chown:
	sudo chown -R $(UID):$(GID) .
deploy:
	docker run --rm -it -v ~/.ssh:/root/.ssh -v ${PWD}:/docs squidfunk/mkdocs-material:7.3.6 gh-deploy
