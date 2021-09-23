FROM	python:3

RUN	set -x \
	# Install the needed packages:
	&& DEBIAN_FRONTEND=noninteractive \
	&& apt update \
	&& apt install --no-install-recommends --assume-yes \
		libmediainfo0v5 \
	&& rm -rf /var/lib/apt/lists/*

WORKDIR	/app

VOLUME	["/app", "/config", "/data", "/www"]

EXPOSE	8080

COPY	docker-entrypoint.sh /usr/local/bin/
ENTRYPOINT	["docker-entrypoint.sh"]

CMD	["python", "/app/main.py"]
