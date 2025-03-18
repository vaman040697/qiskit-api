from fastapi import APIRouter, Query
from googleapiclient.discovery import build
from drive_auth import authenticate_drive

colab_router = APIRouter()

@colab_router.post("/create_colab_notebook")  # <-- New API route for Google Colab
async def create_colab_notebook(name: str = Query("New Notebook")):
    creds = authenticate_drive()
    drive_service = build("drive", "v3", credentials=creds)

    # Create a new Google Colab notebook in Drive
    file_metadata = {
        "name": f"{name}.ipynb",
        "mimeType": "application/vnd.google.colaboratory",
        "parents": ["1wcJ53gfaXy7_Wt97M0hBPTt3vvh14bcB"]
    }

    file = drive_service.files().create(body=file_metadata).execute()

    # Generate a public Colab link
    colab_url = f"https://colab.research.google.com/drive/{file['id']}"

    return {"colab_url": colab_url}
