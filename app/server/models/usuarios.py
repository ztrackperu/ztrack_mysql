from typing import Optional,List
from pydantic import BaseModel, Field

class UsuariosSchema(BaseModel):
    id:int = Field(...)
    usuario: str = Field(...)
    apellidos: str = Field(...)
    nombres: str = Field(...)
    estado: Optional[int] | None =1
    permiso: Optional[int] | None =1
    correo: Optional[str] | None ="admin@zgroup.com.pe"
    password: str = Field(...)
    ultimo_acceso: Optional[str] | None =None
    created_at: Optional[str] | None =None
    updated_at: Optional[str] | None =None

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "usuario": "APEEL",
                "apellidos": "Central", 
                "nombres": "APEEL", 
                "estado": 1, 
                "permiso": 1, 
                "correo": "admin@zgroup.pe", 
                "password": "$10$.V0pXd7XH60V1lUt/NquzUx6KAah1QUu", 
                "ultimo_acceso": "2024-05-03 21:26:35", 
                "created_at": "2024-05-03 21:26:35",  
                "updated_at": "2024-05-03 21:26:35",          
            }
        }

class UpdateUsuariosModel(BaseModel):
    usuario: Optional[str] | None =None
    apellidos: Optional[str] | None =None
    nombres: Optional[str] | None =None
    estado: Optional[int] | None =None
    permiso: Optional[int] | None =None
    correo: Optional[str] | None =None
    password: Optional[str] | None =None
    ultimo_acceso: Optional[str] | None =None
    created_at: Optional[str] | None =None
    updated_at: Optional[str] | None =None

    class Config:
        json_schema_extra = {
            "example": {
                "usuario": "APEEL",
                "apellidos": "Central", 
                "nombres": "APEEL", 
                "estado": 1, 
                "permiso": 1, 
                "correo": "admin@zgroup.pe", 
                "password": "$10$.V0pXd7XH60V1lUt/NquzUx6KAah1QUu", 
                "ultimo_acceso": "2024-05-03 21:26:35", 
                "created_at": "2024-05-03 21:26:35",  
                "updated_at": "2024-05-03 21:26:35",          
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

