from pydantic import BaseModel

# Define the model for the request
class OfficeCodeRequest(BaseModel):
    officecode: str