#!/bin/bash

echo "User authentication..."
gcloud auth login

echo "Settin project..."
gcloud config set project <your-project-id>

echo "Application default authentication..."
gcloud auth application-default login

echo "authentication completed."