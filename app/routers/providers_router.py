from fastapi import APIRouter, HTTPException
from app.models.provider_model import OfficeCodeRequest  # Import the model
import requests

router = APIRouter(
    prefix="/provider",
    tags=["officeCode"],
    responses={404: {"description": "Not found"}},
)

# Example external URL (replace with your actual endpoint)
EXTERNAL_API_URL = "https://external-api.com/office-details/"

@router.post("/office-details")
async def get_office_details(request: OfficeCodeRequest):
    """Fetch office details by office code."""
    officecode = request.officecode

    # Construct the external API URL with the officecode
    external_url = f"{EXTERNAL_API_URL}{officecode}"

    try:
        # Query the external API
        response = requests.get(external_url)

        # Check if the response is successful
        if response.status_code == 200:
            return response.json()  # Return the JSON response from the external API
        else:
            raise HTTPException(status_code=response.status_code, detail="Error from external API")

    except requests.RequestException as e:
        # Handle any errors during the request
        raise HTTPException(status_code=500, detail=f"Failed to connect to external API: {str(e)}")