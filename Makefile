CONTAINER = or/highs
PUSH_TAG = latest

build:
	echo Building $(CONTAINER):$(PUSH_TAG)
	docker build --rm -t $(CONTAINER):$(PUSH_TAG) .
run:
	echo Run bash $(CONTAINER):$(PUSH_TAG)
	docker run --rm -ti \
		-p 81:81 \
		-v ${PWD}:/app $(CONTAINER):$(PUSH_TAG)
run-bash:
	echo Run bash $(CONTAINER):$(PUSH_TAG)
	docker run --rm -ti \
		-p 80:80 \
		-v ${PWD}:/app $(CONTAINER):$(PUSH_TAG) bash
