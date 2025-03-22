# GLOBAL VARIABLES (TO MODIFY)
PROJECT_ID=
REGION=europe-west4
REPO_NAME=test
CONTAINER_NAME=inference_application

# UTILS
define get_version
    grep -m 1 version pyproject.toml | tr -s ' ' | tr -d '"' | tr -d "'" | cut -d' ' -f3
endef

define print_msg
    @tput setaf 2; echo "[$(shell date '+%Y-%m-%d %H:%M:%S')] $(1)"; tput sgr0
endef

TEMPLATE_IMAGE := $(REGION)-docker.pkg.dev/$(PROJECT_ID)/$(REPO_NAME)/$(CONTAINER_NAME)
VERSION := $(shell $(get_version))
FULL_IMAGE := $(TEMPLATE_IMAGE):$(VERSION)

.PHONY: all build deploy help

all: build deploy

build:
	$(call print_msg, "Start of Docker image build...")
	gcloud builds submit --tag "$(FULL_IMAGE)" --region=$(REGION)
	$(call print_msg, "Build successfully completed!")

deploy:
	$(call print_msg, "Start deployment on Cloud Run...")
	gcloud run deploy $(CONTAINER_NAME) \
		--image "$(FULL_IMAGE)" \
		--region $(REGION) \
		--allow-unauthenticated \
		--set-env-vars GCP_PROJECT_ID="$(PROJECT_ID)" \
		--port=8000
	$(call print_msg, "Deploy on Cloud Run successfully completed!")

help:
	@echo "Available commands:"
	@echo "  make build    - Build Docker Image"
	@echo "  make deploy   - Run Deploy on Cloud Run"
	@echo "  make all      - Run both build and deploy"
	@echo "  make help     - Show help message"
