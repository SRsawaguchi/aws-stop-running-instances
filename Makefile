FUNCTION_NAME := stop-running-ec2-rds-instances
ZIP_FILE := build/lambda.zip
SRC_DIR := src

.PHONY: build
build:
	rm -f $(ZIP_FILE) && \
	zip -r $(ZIP_FILE) -j $(SRC_DIR)

.PHONY: deploy
deploy:
	rm -f $(ZIP_FILE) && \
	zip -r $(ZIP_FILE) -j $(SRC_DIR) && \
	aws lambda update-function-code \
		--function-name $(FUNCTION_NAME) \
		--zip-file fileb://$(ZIP_FILE)

.PHONY: invoke
invoke:
	aws lambda invoke --function-name $(FUNCTION_NAME) out --log-type Tail
