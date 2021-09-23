CONFIG_DIR  ?= ${CURDIR}/.config
DATA_DIR    ?= /tmp/cupidon
WWW_DIR     ?= ${CURDIR}/.www
DOCKER_PORT ?= 8080

MOUNT_APP_ANGULAR := --volume ${CURDIR}/angular:/app
MOUNT_APP_PYTHON  := --volume ${CURDIR}/python:/app
MOUNT_CONFIG      := --volume ${CONFIG_DIR}:/config --env CONFIG_DIR=/config
MOUNT_DATA        := --volume ${DATA_DIR}:/data --env DATA_DIR=/data
MOUNT_WWW         := --volume ${WWW_DIR}:/www --env WWW_DIR=/www

DOCKER_COMMON  := --rm ${MOUNT_WWW}
DOCKER_ANGULAR := ${DOCKER_COMMON} ${MOUNT_APP_ANGULAR}
DOCKER_PYTHON  := ${DOCKER_COMMON} ${MOUNT_APP_PYTHON} ${MOUNT_CONFIG} ${MOUNT_DATA} --publish ${DOCKER_PORT}:8080

ifneq (${DOCKER_NETWORK},)
DOCKER_PYTHON  += --network ${DOCKER_NETWORK}
endif

ifneq (${DATA_FILES_DIR},)
DOCKER_PYTHON  += --env DATA_FILES_DIR=${DATA_FILES_DIR}
endif

ifneq (${DATA_MOVIES_DIR},)
DOCKER_PYTHON  += --env DATA_MOVIES_DIR=${DATA_MOVIES_DIR}
endif

ifneq (${DATA_TV_SHOWS_DIR},)
DOCKER_PYTHON  += --env DATA_TV_SHOWS_DIR=${DATA_TV_SHOWS_DIR}
endif

.PHONY: all
all: run-python

.PHONY: bash-python
bash-python: .docker-python .build-angular
	docker run -it ${DOCKER_PYTHON} $(patsubst .%,%,$<) bash

.PHONY: run-python
run-python: .docker-python .build-angular
	docker run -it ${DOCKER_PYTHON} $(patsubst .%,%,$<)

.PHONY: bash-angular
bash-angular: .docker-angular
	docker run -it ${DOCKER_ANGULAR} $(patsubst .%,%,$<) bash

.PHONY: build-angular
build-angular: .docker-angular
	docker run -it ${DOCKER_ANGULAR} $(patsubst .%,%,$<) ng build --output-path=/www --watch

.build-angular: .docker-angular
	docker run ${DOCKER_ANGULAR} $(patsubst .%,%,$<)
	touch $@

.docker-angular .docker-python: .docker-%: %/Dockerfile %/docker-entrypoint.sh | .fix-permissions
	docker build --file $< --tag $(patsubst .%,%,$@) $(dir $<)
	touch $@

.PHONY: .fix-permissions
.fix-permissions:
	git ls-files | xargs dirname | sort -u | xargs chmod 755
	git ls-files | xargs chmod 644
	git ls-files | grep docker-entrypoint.sh | xargs chmod 755

.PHONY: clean
clean:
	rm -f  ${CURDIR}/.build-angular
	rm -f  ${CURDIR}/.docker-angular
	rm -f  ${CURDIR}/.docker-python
	rm -rf ${CURDIR}/angular/node_modules
	rm -f  ${CURDIR}/angular/package-lock.json
	rm -rf ${CURDIR}/python/virtual_environment
