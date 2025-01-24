from fastapi import FastAPI, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv
import anthropic
import base64
import os
from dataclasses import dataclass

app = FastAPI()

@dataclass
class QueryResponse:
    """Class for holding the query response and token usage"""
    text: str
    input_tokens: int = 0
    output_tokens: int = 0

class ClaudePDFQuery:
    def __init__(self):
        """Initialize the Claude PDF Query client"""
        load_dotenv()
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
        self.client = anthropic.Anthropic(api_key=self.api_key)
    
    def _load_pdf(self, file: UploadFile):
        """
        Load and encode a PDF file from an upload.
        
        Args:
            file (UploadFile): Uploaded PDF file
            
        Returns:
            str: Base64 encoded PDF content
        """
        try:
            pdf_bytes = file.file.read()
            return base64.b64encode(pdf_bytes).decode('utf-8')
        except Exception as e:
            raise Exception(f"Error reading PDF file: {str(e)}")
    
    def query_pdf(self, pdf_file: UploadFile, query_text: str):
        """
        Query a PDF file using Claude API.
        
        Args:
            pdf_file (UploadFile): Uploaded PDF file
            query_text (str): The question or prompt to ask about the PDF
            
        Returns:
            QueryResponse: Object containing response text and token usage
        """
        try:
            pdf_data = self._load_pdf(pdf_file)
            
            message = self.client.beta.messages.create(
                model="claude-3-5-sonnet-20241022",
                betas=["pdfs-2024-09-25", "prompt-caching-2024-07-31"],
                max_tokens=1024,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "document",
                                "source": {
                                    "type": "base64",
                                    "media_type": "application/pdf",
                                    "data": pdf_data
                                },
                                "cache_control": {"type": "ephemeral"}
                            },
                            {
                                "type": "text",
                                "text": query_text
                            }
                        ]
                    }
                ],
            )
            
            return QueryResponse(
                text=message.content[0].text,
                # Uncomment if token usage is available
                # input_tokens=message.usage.input_tokens,
                # output_tokens=message.usage.output_tokens
            )
            
        except Exception as e:
            raise Exception(f"Error querying PDF: {str(e)}")

# Initialize the query class
pdf_query = ClaudePDFQuery()

@app.post("/query-pdf/")
async def query_pdf_endpoint(pdf_file: UploadFile, query_text: str = Form(...)):
    """
    API endpoint to query a PDF file.
    
    Args:
        pdf_file (UploadFile): The uploaded PDF file.
        query_text (str): The text query to ask about the PDF.
    
    Returns:
        JSONResponse: Contains the response text and token usage.
    """
    try:
        response = pdf_query.query_pdf(pdf_file, query_text)
        return JSONResponse(content={
            "response": response.text,
            "input_tokens": response.input_tokens,
            "output_tokens": response.output_tokens
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
