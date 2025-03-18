from fastapi import FastAPI, Query
import requests
from bs4 import BeautifulSoup
from fastapi.openapi.utils import get_openapi

app = FastAPI(
    title="Qiskit API",
    description="Retrieves relevant documentation from the latest Qiskit API.",
    version="1.0.0"
)

# Define OpenAPI schema in the correct format for OpenAI
def custom_openapi():
    openapi_schema = {
        "openapi": "3.1.0",
        "info": {
            "title": "Qiskit API",
            "description": "Searches the latest Qiskit documentation dynamically.",
            "version": "1.0.0"
        },
        "servers": [
            {"url": "https://qiskit-api.onrender.com"}  # Ensure OpenAI detects the API
        ],
        "paths": {
            "/search_qiskit": {
                "get": {
                    "summary": "Search Qiskit documentation",
                    "description": "Retrieve relevant sections from Qiskit documentation.",
                    "operationId": "SearchQiskitDocs",
                    "parameters": [
                        {
                            "name": "query",
                            "in": "query",
                            "description": "The search query related to Qiskit documentation.",
                            "required": True,
                            "schema": {"type": "string"}
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Successful response",
                            "content": {
                                "application/json": {
                                    "example": {
                                        "query": "quantum gates",
                                        "results": [
                                            {"url": "https://docs.quantum.ibm.com/api/qiskit/", "snippet": "Qiskit SDK API documentation..."}
                                        ]
                                    }
                                }
                            }
                        }
                    },
                    "deprecated": False
                }
            }
        },
        "components": {  # Fix: Ensure schemas object exists
            "schemas": {}
        }
    }
    return openapi_schema

app.openapi = custom_openapi  # Apply OpenAPI format fix
