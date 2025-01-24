# PDF Process API

A FastAPI-based REST API that enables querying PDF documents using Anthropic's Claude 3 Sonnet model. This API allows users to upload PDF files and ask questions about their content, leveraging Claude's advanced capabilities to understand and analyze PDF documents.

## Features

- PDF document processing using Claude 3 Sonnet
- Simple REST API endpoint for PDF queries
- Base64 PDF encoding for secure transmission
- Environment-based configuration
- Error handling and validation

## Requirements

- Python 3.7+
- FastAPI
- Uvicorn (ASGI server)
- Anthropic Python SDK
- python-dotenv

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/pdf-process-api.git
cd pdf-process-api
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root and add your Anthropic API key:
```
ANTHROPIC_API_KEY=your_api_key_here
```

## Usage

1. Start the API server:
```bash
uvicorn api:app --reload
```

2. The API will be available at `http://localhost:8000`

3. Use the `/query-pdf/` endpoint to submit queries about PDF documents:

```bash
curl -X POST "http://localhost:8000/query-pdf/" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "pdf_file=@/path/to/your/document.pdf" \
  -F "query_text=What is this document about?"
```

## API Documentation

### POST /query-pdf/

Query a PDF document using Claude 3 Sonnet.

#### Request

- Content-Type: `multipart/form-data`
- Parameters:
  - `pdf_file`: PDF file upload (required)
  - `query_text`: String query about the PDF content (required)

#### Response

```json
{
    "response": "Claude's analysis of the PDF based on the query",
}
```

#### Error Response

```json
{
    "detail": "Error message describing what went wrong"
}
```

## Technical Details

The API uses Claude 3 Sonnet (claude-3-5-sonnet-20241022) with the following beta features:
- pdfs-2024-09-25: Enhanced PDF processing capabilities
- prompt-caching-2024-07-31: Improved response caching

The maximum response length is set to 1024 tokens to ensure reasonable response times and resource usage.
