
SHELL = /bin/bash

build:
	docker build --tag lambda:latest .
	docker run \
		--name lambda \
		-w /tmp \
		--volume $(shell pwd)/bin:/tmp/bin \
		--volume $(shell pwd)/:/local \
		--env PACKAGE_TMP=/tmp/package \
		--env PACKAGE_PATH=/local/package.zip \
		-itd lambda:latest \
		bash
	docker exec -it lambda bash '/tmp/bin/package.sh'
	docker stop lambda
	docker rm lambda

shell:
	docker build --tag lambda:latest .
	docker run --name docker  \
		--volume $(shell pwd)/:/local \
		--rm -it lambda:latest bash

clean:
	docker stop lambda
	docker rm lambda
