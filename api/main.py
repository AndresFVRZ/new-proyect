from fastapi import FastAPI
from metodos import consultarMotos

app = FastAPI(title="API de Motos", description="Sistema de venta de motos", version="1.0.0")

# Incluir todos los routers
app.include_router(consultarMotos.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {
        "message": "API de Motos - FastAPI",
        "endpoints": {
            "marcas": "/api/v1/marcas",
            "motos": "/api/v1/motos",
            "clientes": "/api/v1/clientes",
            "ventas": "/api/v1/ventas",
            "detalles": "/api/v1/detalles",
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "ok", "database": "motos"}

# Para ver rutas registradas
@app.on_event("startup")
async def startup_event():
    print("\n" + "="*50)
    print("🚀 API DE MOTOS INICIADA")
    print("="*50)
    for route in app.routes:
        if hasattr(route, "methods"):
            print(f"{route.methods} - {route.path}")
    print("="*50 + "\n")