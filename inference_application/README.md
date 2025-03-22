# Inference Application

## Repository Structure

This section describes the structure of the repository and the purpose of each directory and file.

## Root Directory
* **config.ini** - Configuration file for global settings.
* **Dockerfile** - Defines the Docker image build process.
* **entry_point.sh** - Shell script to start the application.
* **Makefile** - Automation tool for build and management tasks.
* **pyproject.toml** - Python project configuration file.
* **README.md** - Project documentation (this file).

### src/

Contains the main source code of the project, organized into modules.

### agents/
* **notes_agent.py** - Contains logic for handling note-related agents.

### controller/

* **ml/** - Submodule for machine learning models.
* **mistral_ocr.py** - Contains MistralClient that uses the new *mistral-ocr-latest* in order to extract text from PDFs.
* **domain_predictor.py** - Contains DomainPredictor class that invokes predictions.

### models/
* **base.py** - Contains base model definitions for api pourposes.
* **notes.py** - Contains models for handling medical notes extracted from PDFs.

### routes/
* **classifier.py** - Manages classification-related routes.
* **globals.py** - Stores global variables and constants.
* **main.py** - Main entry point for defining routes.
* **utils.py** - Contains utility functions used across the application.

### Summary

This modular structure ensures the project is organized, scalable, and easy to maintain. Each component is placed in its relevant directory to promote clean code practices and separation of concerns.

<br>

---

<br><br>

# Setup
This Applicaiton uses Mistral AI OCR model in order to read pdf files, to be able to work with the api you must

For Mistral OCR:
* Create an account in https://auth.mistral.ai/ui/login
* Create an API Key https://console.mistral.ai/inference_application-keys
* Put it in config.ini file

For Gemini:
* Create a Service Account (with VertexAI Admin permissions for semplicity)
* Add new SA API Key, download and save creds.json key and put in **/agents** folder

#### Note
For this demo I avoided the best practice of using a Secret manager to avoid burdening the code.

<br>

# Local Installation and Run
Create Virtual Environment in `/inference_application`
```bash
virtualenv .venv -p python3.12
```
Activate Virtual Environment
```bash
source .venv/bin/activate
```
Install packages
```bash
pip install -e .
```
### Usage
Run FastAPI server
```bash
 fastapi run src/main.py
```

Watch auto-generated docs and try APIs by visiting `http://0.0.0.0:8000/docs`

<br><br>

# Docker
## Deploying on GCP (Cloud Run)

In addition if you want to deploy Docker container in Google Cloud Cloud Run
* Modify GLOBAL VARIABLES in order to attach your project
* Go to Google Cloud Artifact Registry and Create Repository with Docker Format (and Region e.g. europe-west4)

Then

``` bash
make build
make deploy
```
or

``` bash
make all
```

### Curl call (single file)
```bash
curl -X 'POST' \
  'https:/<cloud-run-endpoint>/classifier/docu_predict/' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'files=@sample1 (Gastroenterology,Urology).pdf;type=application/pdf' \
  -F 'files=@Sample2 (Neurology,Orthopedic,Radiology).pdf;type=application/pdf'
  ```
### Curl call (multiple files)
```bash
curl -X 'POST' \
  'https:/<cloud-run-endpoint>/classifier/docu_predict/' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'files=@test1.pdf;type=application/pdf' \
  -F 'files=@test2.pdf;type=application/pdf'
  ```
<br>

## Deploy locally

``` bash
docker build -t nlp-inference_application:latest .
```


``` bash
docker run -d -p 8000:8000 --name nlp-inference_application nlp-inference_application:latest
```

### Curl call (single file)
```bash
curl -X 'POST' \
  'http://localhost:8000/classifier/docu_predict/' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'files=@sample1.pdf;type=application/pdf'
  ```

### Curl call (multiple files)
```bash
curl -X 'POST' \
  'http://localhost:8000/classifier/docu_predict/' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'files=@sample1.pdf;type=application/pdf' \
  -F 'files=@Sample2.pdf;type=application/pdf'
  ```