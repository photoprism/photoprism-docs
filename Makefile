.PHONY: ;
.ONESHELL: ;             # recipes execute in same shell
.NOTPARALLEL: ;          # wait for this target to finish
.EXPORT_ALL_VARIABLES: ; # send all vars to shell

UID := $(shell id -u)
GID := $(shell id -g)

all: pull deploy chown
watch:
	docker run --rm -it -p 8000:8000 -v ${PWD}:/docs squidfunk/mkdocs-material
pull:
	docker pull squidfunk/mkdocs-material
chown:
	sudo chown -R $(UID):$(GID) .
deploy:
	docker run --rm -it -v ~/.ssh:/root/.ssh -v ${PWD}:/docs squidfunk/mkdocs-material gh-deploy
