from pydantic import BaseModel
from typing import Optional, List
from datetime import date

# ===== MARCA SCHEMAS =====
class MarcaBase(BaseModel):
    nombre: str
    pais_origen: Optional[str] = None

class MarcaCreate(MarcaBase):
    pass

class Marca(MarcaBase):
    id_marca: int
    class Config:
        from_attributes = True

# ===== MOTO SCHEMAS =====
class MotoBase(BaseModel):
    modelo: str
    año: Optional[int] = None
    cilindraje: Optional[int] = None
    precio: Optional[float] = None
    id_marca: int

class MotoCreate(MotoBase):
    pass

class Moto(MotoBase):
    id_moto: int
    class Config:
        from_attributes = True

class MotoConMarca(Moto):
    marca: Optional[Marca] = None

# ===== CLIENTE SCHEMAS =====
class ClienteBase(BaseModel):
    nombre: str
    telefono: Optional[str] = None
    correo: Optional[str] = None
    direccion: Optional[str] = None

class ClienteCreate(ClienteBase):
    pass

class Cliente(ClienteBase):
    id_cliente: int
    class Config:
        from_attributes = True

# ===== VENTA SCHEMAS =====
class VentaBase(BaseModel):
    fecha_venta: date
    id_cliente: int
    total: Optional[float] = None

class VentaCreate(VentaBase):
    pass

class Venta(VentaBase):
    id_venta: int
    class Config:
        from_attributes = True

# ===== DETALLE VENTA SCHEMAS =====
class DetalleVentaBase(BaseModel):
    id_venta: int
    id_moto: int
    cantidad: int = 1
    precio_unitario: float

class DetalleVentaCreate(DetalleVentaBase):
    pass

class DetalleVenta(DetalleVentaBase):
    id_detalle: int
    class Config:
        from_attributes = True

# ===== SCHEMAS COMPUESTOS =====
class VentaCompleta(Venta):
    cliente: Optional[Cliente] = None
    detalles: List[DetalleVenta] = []