from fastapi import FastAPI, Query
import requests
from bs4 import BeautifulSoup
from fastapi.openapi.utils import get_openapi

app = FastAPI(
    title="Qiskit API",
    description="Retrieves relevant documentation from the latest Qiskit API.",
    version="1.0.0"
)

# Define OpenAPI schema in the correct format
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Qiskit API",
        version="1.0.0",
        description="Search the latest Qiskit documentation dynamically.",
        routes=app.routes,
    )
    openapi_schema["openapi"] = "3.1.0"  # Set OpenAPI version
    openapi_schema["servers"] = [{"url": "https://qiskit-api.onrender.com"}]  # Ensure OpenAI finds the API
    openapi_schema["paths"] = {
        "/search_qiskit": {
            "get": {
                "description": "Search Qiskit documentation for relevant information.",
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
                "deprecated": False
            }
        }
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi  # Apply OpenAPI format fix
