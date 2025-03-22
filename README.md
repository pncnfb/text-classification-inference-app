# Text Classification Inference App

## Goal

This project focuses on building an **NLP classification model** to categorize medical notes into five clinical domains. The trained model is then integrated into a containerized inference application that processes PDF files, extracts relevant text, and outputs classification labels. The aim is to create a scalable, well-documented solution that handles *class imbalance* and varying document layouts effectively.

## Repository Structure

This section describes the structure of the repository and the purpose of each directory and file.

* **/inference_application** - Containerized Inference Application
* **/sample_pdfs** - sample PDFs (there are no changes from the original)
* **/test** - test data (there are no changes from the original)
* **/train** - train data, from the ‘**00_data_augmentation.ipynb**’ notebook, the */augment* folder and the *train_data_aug.csv* file are generated
* **auth.sh** - util script for Google Cloud Login

## Description
The natural order of visualization of this repository is:

* **00_data_augmentation.ipynb**: Given the data imbalance, I thought that performing data augmentation with an LLM (Gemini) could be a good starting point to fill in any gaps.
* **01_npl_model.ipynb**: After the data augmentation, I trained a model to solve the classification task.
* **/inference_application**: Lastly, there's the inference application developed with FastAPI, which combines the use of Mistral OCR (they say it's the best-performing model!), Gemini (for splitting notes based on the semantic text of each PDF), and the NLP classification model to solve the assigned task