from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from typing import Optional

#aqui pedimos las funciones que incluyen nuestro CRUD
from server.funciones.contenedores import (
    retrieve_contenedores,
    lista_contenedores,
    lista_contenedores_empresa,
    lista_contenedores_data,
    validar_live,
    contenedor_data,
    contenedor_telemetria,
    validar_telemetria,
    lista_contenedores_empresa_2xl,
    actualizar_data
)
#Aqui importamos el modelo necesario para la clase 
from server.models.contenedores import (
    ErrorResponseModel,
    ResponseModel,
    ValidarLive,
    contenedor_base,
)
#aqui se definen las rutas de la API REST
router = APIRouter()

@router.get("/validar_telemetria/{id}", response_description="contenedores recuperados")
async def validar_telemetria_ok(id: int):
    notificacions = await validar_telemetria(id)
    if notificacions:
        return notificacions
    return 0

@router.post("/actualizar_data", response_description="Datos Listados de los usuarios.")
async def actualizar_data_ok(datos: contenedor_base = Body(...)):
    datos = jsonable_encoder(datos) 
    new_notificacion = await actualizar_data(datos)
    if  new_notificacion:
        return new_notificacion
    else :
        return 0

@router.get("/", response_description="contenedores recuperados")
async def get_contenedores():
    notificacions = await retrieve_contenedores()
    if notificacions:
        return ResponseModel(notificacions, "Datos de los contenedores recuperados exitosamente.")
    return ResponseModel(notificacions, "Lista vacía devuelta")

@router.get("/ListaContenedores/{id}", response_description="contenedores recuperados")
async def get_lista_contenedores(id: int):
    notificacions = await lista_contenedores(id)
    if notificacions:
        return ResponseModel(notificacions, "Datos de los contenedores recuperados exitosamente.")
    return ResponseModel(notificacions, "Lista vacía devuelta")

@router.get("/ListaDispositivoEmpresa/{id}", response_description="contenedores recuperados")
async def get_lista_contenedores_empresa(id: int):
    notificacions = await lista_contenedores_empresa(id)
    if notificacions:
        return ResponseModel(notificacions, "Datos de los contenedores recuperados exitosamente.")
    return ResponseModel(notificacions, "Lista vacía devuelta")

@router.get("/ListaDispositivoEmpresa2xl/{id}", response_description="contenedores recuperados")
async def get_lista_contenedores_empresa_2xl(id: int, gmt: Optional[str] = "-5"):
    notificacions = await lista_contenedores_empresa_2xl(id,gmt)
    if notificacions:
        return ResponseModel(notificacions, "Datos de los contenedores recuperados exitosamente.")
    return ResponseModel(notificacions, "Lista vacía devuelta")

@router.get("/ExtraerDatos/{id}", response_description="data recuperados")
async def get_extraer_datos_empresa(id: int):
    notificacions = await lista_contenedores_data(id)
    if notificacions:
        return ResponseModel(notificacions, "Datos de los contenedores recuperados exitosamente.")
    return ResponseModel(notificacions, "Lista vacía devuelta")

@router.post("/VerificarLive/", response_description="Datos de los notificacion agregados a la base de datos.")
#La funcion espera "ConceptoOTSchema"
async def validar_live_data(notificacion: ValidarLive = Body(...)):
    #convertir en json
    #notificacion = jsonable_encoder(notificacion)   
    #print(notificacion)
    #enviar a la funcion añadir  
    new_notificacion = await validar_live(notificacion)
    return ResponseModel(new_notificacion, "ok")

#contenedor_data
@router.get("/ContenedorData/{id}", response_description="data recuperados")
async def get_dato_contenedor(id: str):
    notificacions = await contenedor_data(id)
    if notificacions:
        return ResponseModel(notificacions, "Datos de los contenedores recuperados exitosamente.")
    return ResponseModel(notificacions, "Lista vacía devuelta")


@router.get("/DatoTelemetria/{id}", response_description="data recuperados")
async def get_extraer_datos_telemetria(id: int):
    notificacions = await contenedor_telemetria(id)
    if notificacions:
        return ResponseModel(notificacions, "Datos de los contenedores recuperados exitosamente.")
    return ResponseModel(notificacions, "Lista vacía devuelta")