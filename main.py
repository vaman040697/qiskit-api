from fastapi import FastAPI, Query
import requests
from bs4 import BeautifulSoup
from fastapi.openapi.utils import get_openapi
from colab_api import colab_router  # Import the new API module

app = FastAPI(
    title="Qiskit API",
    description="Retrieves relevant documentation from the latest Qiskit API.",
    version="1.0.0"
)

@app.get("/search_qiskit")  # Ensure this matches exactly
async def search_qiskit(query: str = Query(...)):
    return {"query": query, "results": [{"url": "https://docs.quantum.ibm.com/api/qiskit/", "snippet": "Qiskit SDK API documentation..."}]}

# Include Google Colab API without affecting Qiskit functionality
app.include_router(colab_router)

# Custom OpenAPI Schema
def custom_openapi():
    openapi_schema = {
        "openapi": "3.1.0",
        "info": {
            "title": "Qiskit API",
            "description": "Searches the latest Qiskit documentation dynamically.",
            "version": "1.0.0"
        },
        "servers": [{"url": "https://qiskit-api.onrender.com"}],
        "paths": {
            "/search_qiskit": {  # Make sure this matches FastAPI route
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
                                        "results": [{"url": "https://docs.quantum.ibm.com/api/qiskit/", "snippet": "Qiskit SDK API documentation..."}]
                                    }
                                }
                            }
                        }
                    },
                    "deprecated": False
                }
            }
        },
        "components": {"schemas": {}}
    }
    return openapi_schema

app.openapi = custom_openapi  # Apply OpenAPI fix
