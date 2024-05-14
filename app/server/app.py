from fastapi import FastAPI

from server.routes.usuarios import router as UsuariosRouter
from server.routes.contenedores import router as ContenedoresRouter

app = FastAPI(
    title="Integracion ZTRACK MYSQL",
    summary="Modulos de datos bidireccional",
    version="0.0.1",

)

#añadir el conjunto de rutas de notificaciones
app.include_router(UsuariosRouter, tags=["usuarios"], prefix="/usuarios")
app.include_router(ContenedoresRouter, tags=["contenedores"], prefix="/contenedores")


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app ztrack by mysql!"}
