# PDF Question Extractor and Rephraser

This project is a Python-based application that extracts questions, options, correct answers, and justifications from PDF documents, processes the text (including table recognition and rephrasing), and stores the results in a Firebase Firestore database and a Word document.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)

## Features

- Extracts text, questions, options, correct answers, and justifications from PDF files.
- Detects and rephrases tables within the extracted text.
- Processes images found in PDF documents and uploads them to Firebase Storage.
- Saves the extracted and processed content into a Firestore database and Word documents.

## Requirements

- Python 3.8 or higher
- Firebase Admin SDK credentials
- OpenAI API key
- Dependencies listed in `requirements.txt`

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/pdf-question-extractor.git
   cd pdf-question-extractor
   ```

2. **Set up a virtual environment (optional but recommended):**

    ```bash
    
    python -m venv .venv
    source .venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3. **Install the required Python packages:**
  
    ```bash
    pip install -r requirements.txt
    ```
4. **Create the necessary directories:**

    ```bash
    mkdir output
    mkdir images
    mkdir pdfs
    ```
    Place your PDF files in the pdfs directory.

5. **Prepare your Firebase credentials:**

    Download your Firebase Admin SDK credentials (firebase_credentials.json) and place it in the root directory.
    <br>[Watch this video on YouTube](https://www.youtube.com/watch?v=qsFYq_1BQdk&t=290s)

## Usage
1. **Set up environment variables:**

    Create a .env file in the root directory with the following content:
  
     ```env
     FIRESTORE_BUCKET=your-firebase-bucket-name
     OPENAI_API_KEY=your-openai-api-key
     ```
2. **Run the extraction process:**

    ```bash
    python extract_pdfs.py
    ```
    This will process all PDF files in the pdfs directory, extract questions, options, correct answers, and justifications, and save the output to Firebase Firestore and Word documents.

## Configuration
1. **Directory Structure**
    - pdfs/: Directory containing PDF files to be processed.
    - images/: Directory where extracted images from PDFs will be temporarily stored.
    - output/: Directory where output files (output.json, output_with_tables.json, output.docx, output_with_tables.docx) will be saved.

3. **Firebase Configuration**
    - Ensure that your Firebase project is set up and your credentials are correctly configured in firebase_credentials.json.
