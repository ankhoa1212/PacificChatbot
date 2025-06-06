# PacificChatbot

PacificChatbot is a conversational AI chatbot application built with Python, Flask, and a custom-trained neural network.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running Locally with Flask](#running-locally-with-flask)
- [Conclusion and Results](#conclusion-and-results)

## Features

- Conversational chatbot interface
- Flask-powered backend
- Easy local development and testing
- Utilities for data collection and cleaning
    - [Webpage Data Collection](https://github.com/ankhoa1212/PacificChatbot/tree/main/Data_cleaning)
    - [PDF Data Collection](https://github.com/ankhoa1212/PacificChatbot/tree/main/pdf_data_collector)
    - [Data Cleaning Pipeline](https://github.com/ankhoa1212/PacificChatbot/tree/main/Clean_Web_Data)
- [Formatted question-answer dataset](https://github.com/ankhoa1212/PacificChatbot/tree/main/Dataset)

## Prerequisites

- [Python 3](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/)

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/ankhoa1212/PacificChatbot.git
    cd PacificChatbot
    ```

2. **Create and activate a virtual environment (optional but recommended):**
    ```bash
    python -m venv venv
    # On Windows:
    venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```

3. **Install dependencies:**
    ```bash
    pip install flask
    pip install torch
    ```

## Running Locally with Flask

1. **Set the Flask app environment variable:**
    ```bash
    # On Windows:
    set FLASK_APP=app.py
    # On macOS/Linux:
    export FLASK_APP=app.py
    ```

2. **(Optional) Enable debug mode:**
    ```bash
    # On Windows:
    set FLASK_ENV=development
    # On macOS/Linux:
    export FLASK_ENV=development
    ```
3. **Navigate to the project directory (if not already there):**
    ```bash
    cd PacificChatbot
    ```

4. **Start the Flask server:**
    ```bash
    flask run
    ```

5. **Access the chatbot:**
    Open your browser and go to [http://localhost:5000](http://localhost:5000)

## Conclusion and Results
Implementing a custom neural network can be a preferred solution over a language model when dealing with a specific data for task-specific queries. More details of the project can be found in the [research publication](https://thesai.org/Publications/ViewPaper?Volume=15&Issue=6&Code=ijacsa&SerialNo=6).

To explore potential data features and machine learning methodologies, some work was done on [binary classification tasks](https://github.com/ankhoa1212/PacificChatbot/tree/main/Project_Summary/Summary.ipynb).