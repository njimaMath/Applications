# Referee Automation

A web application for academic paper review automation that helps convert PDF documents to LaTeX and check for grammatical errors.

## Features

- **PDF to LaTeX Conversion**: Upload PDF files and convert them to LaTeX format
- **Grammar and Spell Checking**: Check converted LaTeX files for grammatical errors and typos
- **Download LaTeX Files**: Download the converted LaTeX files
- **Error Reporting**: View detailed error reports with line numbers and suggestions

## Installation

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables:
   ```bash
   cp .env.template .env
   # Edit .env and add your GROQ_API_KEY
   ```

3. Run the application:
   ```bash
   python app.py
   ```

4. Open your browser and go to `http://localhost:5000`

## Usage

1. **Upload a PDF**: Click "Choose File" and select a PDF document
2. **Convert to LaTeX**: Click "Upload PDF" to convert the document
3. **Download LaTeX** (optional): Choose whether to download the converted LaTeX file
4. **Check for Errors**: Click "List Typos and Grammatical Errors" to analyze the document
5. **Review Results**: View the error report with suggestions for improvement

## Dependencies

- Flask: Web framework
- PyPDF2: PDF text extraction
- requests: HTTP client for API calls
- python-dotenv: Environment variable management

## API Requirements

This application requires a GROQ API key for grammar checking functionality. You can obtain one from [OpenRouter](https://openrouter.ai/).