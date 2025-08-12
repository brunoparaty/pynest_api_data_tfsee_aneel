from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from src.app_module import AppModule
from nest.core import PyNestFactory
import uvicorn

nest_app = PyNestFactory.create(AppModule)

app: FastAPI = nest_app.get_server()

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    print(f"Ocorreu um erro inesperado: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Ocorreu um erro interno no servidor."}
    )

if __name__ == '__main__':
    print("Iniciando o servidor da API com Uvicorn...")
    uvicorn.run(
        'src.main:app', 
        host="0.0.0.0",
        port=8000,
        reload=True
    )