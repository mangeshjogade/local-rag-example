# Local RAG (Retrieval-Augmented Generation) Project

This project implements a local Retrieval-Augmented Generation (RAG) system using LangChain and OpenAI's GPT models to provide information about dashboards based on a local document.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Contributing](#contributing)
- [License](#license)

## Installation

Follow these steps to set up the project on your local machine:

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/local-rag-project.git
   cd local-rag-project
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```bash
     source venv/bin/activate
     ```

4. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Set up your OpenAI API key:
   - Create a `.env` file in the project root
   - Add your OpenAI API key to the file:
     ```bash
     OPENAI_API_KEY=your_api_key_here
     ```

6. Alternatively, you can set up your OpenAI API key in the `local_rag.py` file:
   - Open the `local_rag.py` file in your preferred text editor
   - Locate the line where the OpenAI API key is set (usually near the top of the file)
   - Replace the placeholder with your actual API key:
     ```python
     os.environ["OPENAI_API_KEY"] = "your_api_key_here"
     ```
   - Save the file

Note: It's generally safer to use environment variables (as in step 5) rather than hardcoding the API key in your script. Only use this method for local development and never commit your API key to version control.

## Usage

To run the project, follow these steps:

1. Make sure you're in the project directory and your virtual environment is activated.

2. Prepare your sample document:
   - Create a file named `sample_document.txt` in the project root
   - Add the content about dashboards that you want to use for retrieval

3. Run the main Python script:
   ```bash
   python local_rag.py
   ```

4. The script will process the document and wait for your questions. You can ask questions about dashboards, and the system will provide answers based on the information in the sample document.

Example usage:

```python
# This is automatically run when you execute local_rag.py
ask_question("Can you provide me the link to the dashboard that shows the sales performance?")
ask_question("Can you provide dashboard for customer lifetime value?")
```

## Features

- Local document processing and embedding
- Retrieval-Augmented Generation using OpenAI's GPT models
- Custom tool for retrieving dashboard information
- Interactive question-answering about dashboards

