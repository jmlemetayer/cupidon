# Angular builder stage
FROM	node:lts AS builder

RUN	npm install -g @angular/cli

WORKDIR	/build

COPY	angular/ .

RUN	set -x \
	&& find -type d -exec chmod 755 {} + \
	&& find -type f -exec chmod 644 {} + \
	&& npm install \
	&& ng build --configuration production --output-path /www

# Python application
FROM	python:3

COPY	--from=builder /www /www

RUN	set -x \
	# Install the needed packages:
	&& DEBIAN_FRONTEND=noninteractive \
	&& apt update \
	&& apt install --no-install-recommends --assume-yes \
		libmediainfo0v5 \
	&& rm -rf /var/lib/apt/lists/*

WORKDIR	/app

COPY	python/requirements.txt .

RUN	pip install --no-cache-dir -r requirements.txt

COPY	python/ .

RUN	set -x \
	&& find -type d -exec chmod 755 {} + \
	&& find -type f -exec chmod 644 {} +

VOLUME	["/config", "/downloads"]

EXPOSE	8080

CMD	["python", "/app/main.py"]
