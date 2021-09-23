FROM	node:lts

RUN	set -x \
	&& npm install -g @angular/cli

WORKDIR	/app

VOLUME	["/app", "/www"]

COPY	docker-entrypoint.sh /usr/local/bin/
ENTRYPOINT	["docker-entrypoint.sh"]

CMD	["ng", "build", "--configuration=production", "--output-path=/www"]
