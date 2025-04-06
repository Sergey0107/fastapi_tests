from pydantic import BaseModel 


class ErrorResponse(BaseModel): 
    error_code: int 
    error_message: str 
    error_details: str | None = None 