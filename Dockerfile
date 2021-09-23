# Angular builder stage
FROM	node:lts AS builder

WORKDIR	/build

COPY	angular/ .

RUN	set -x \
	&& npm install -g @angular/cli \
	&& npm install \
	&& ng build --configuration production --output-path /www

# Python application
FROM	python:3

COPY	--from=builder /www /www

COPY	python/ /app

RUN	set -x \
	# Install the needed packages:
	&& DEBIAN_FRONTEND=noninteractive \
	&& apt update \
	&& apt install --no-install-recommends --assume-yes \
		libmediainfo0v5 \
	&& rm -rf /var/lib/apt/lists/* \
	# Install the python requirements
	&& pip install --no-cache-dir -r /app/requirements.txt

WORKDIR	/config

VOLUME	["/config", "/data"]

EXPOSE	8080

COPY	docker-entrypoint.sh /usr/local/bin/
ENTRYPOINT	["docker-entrypoint.sh"]

CMD	["python", "/app/main.py"]
