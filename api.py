# claude_pdf_query.py

import anthropic
import base64
from dotenv import load_dotenv
import os
from dataclasses import dataclass

@dataclass
class QueryResponse:
    """Class for holding the query response and token usage"""
    text: str
    input_tokens: int
    output_tokens: int

class ClaudePDFQuery:
    def __init__(self):
        """Initialize the Claude PDF Query client"""
        load_dotenv()
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
        self.client = anthropic.Anthropic(api_key=self.api_key)
    
    def _load_pdf(self, pdf_path):
        """
        Load and encode a local PDF file.
        
        Args:
            pdf_path (str): Path to the local PDF file
            
        Returns:
            str: Base64 encoded PDF content
        """
        try:
            with open(pdf_path, 'rb') as file:
                pdf_bytes = file.read()
                return base64.b64encode(pdf_bytes).decode('utf-8')
        except FileNotFoundError:
            raise FileNotFoundError(f"Could not find PDF file at: {pdf_path}")
        except Exception as e:
            raise Exception(f"Error reading PDF file: {str(e)}")
    
    def query_pdf(self, pdf_path, query_text):
        """
        Query a PDF file using Claude API.
        
        Args:
            pdf_path (str): Path to the local PDF file
            query_text (str): The question or prompt to ask about the PDF
            
        Returns:
            QueryResponse: Object containing response text and token usage
        """
        try:
            pdf_data = self._load_pdf(pdf_path)
            
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
                #input_tokens=message.usage.input_tokens,
                #output_tokens=message.usage.output_tokens
            )
            
        except Exception as e:
            raise Exception(f"Error querying PDF: {str(e)}")