from fastapi import FastAPI, Request, HTTPException 
from fastapi.responses import JSONResponse

from schemas import ErrorResponse


app = FastAPI()


class CustomExceptionA(HTTPException): 
    def __init__(self, detail: str, status_code: int = 404): 
        super().__init__(detail=detail, status_code=status_code) 


class CustomExceptionB(HTTPException): 
    def __init__(self, detail: str, status_code: int = 400): 
        super().__init__(detail=detail, status_code=status_code) 


@app.exception_handler(CustomExceptionA) 
async def custom_exc_a(request: Request, exc: ErrorResponse): 
    return JSONResponse(
        status_code=exc.status_code, 
        content={"error": exc.detail}
    )


@app.exception_handler(CustomExceptionB)
async def custom_exc_b(request: Request, exc: ErrorResponse): 
    return JSONResponse(
        status_code=exc.status_code, 
        content={"error": exc.detail}
    )


@app.get("/items/{item_id}")
async def get_item(item_id: int): 
    if item_id == 69: 
        raise CustomExceptionA(status_code=404, detail="item not found")
    return {"message": f"id: {item_id}"}


@app.get("/root")
async def main(): 
    raise CustomExceptionB(status_code=400, detail="Bad request")