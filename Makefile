.PHONY: all pull update-mkdocs-material watch deploy chown;

UID := $(shell id -u)
GID := $(shell id -g)

all: pull deploy chown
chown:
	sudo chown -R $(UID):$(GID) .
pull:
	docker pull photoprism/mkdocs-material:latest
update-mkdocs-material:
	docker pull squidfunk/mkdocs-material:latest
	docker build --no-cache --pull -t photoprism/mkdocs-material:latest -f Dockerfile .
	docker push photoprism/mkdocs-material:latest
watch:
	docker run --rm -u $(UID):$(GID) -it -p 8000:8000 -v ${PWD}:/docs photoprism/mkdocs-material:latest
deploy:
	docker run --rm -u 0:0 -it -v ~/.ssh/id_rsa:/root/.ssh/id_rsa:ro -v ~/.ssh/id_rsa.pub:/root/.ssh/id_rsa.pub:ro  -v ${PWD}:/docs photoprism/mkdocs-material:latest gh-deploy
