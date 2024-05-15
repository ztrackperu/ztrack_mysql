from typing import Optional,List
from pydantic import BaseModel, Field

class ValidarLive(BaseModel):
    data:List = Field(...)
    class Config:
        json_schema_extra = {
            "example": {
                "data": [
                    {
                        "telemetria_id":21,
                        "ultimo" :"12:12:12T2024-05-12"
                    },
                    {
                        "telemetria_id":24,
                        "ultimo" :"14:12:12T2024-05-12"
                    }
                ], 
            }
        }

#respuesta cuando todo esta bien
def ResponseModel(data, message):
    return {
        "data": data,
        "code": 200,
        "message": message,
    }

#respuesta cuando algo sale mal 
def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}

