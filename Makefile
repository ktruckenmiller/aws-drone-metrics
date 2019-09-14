
develop: build
	docker run -it \
		-v ${PWD}:/app \
		-e AWS_DEFAULT_REGION=us-west-2 \
		-e IAM_ROLE \
		aws-drone-metrics sh

build:
	docker build -t aws-drone-metrics .
