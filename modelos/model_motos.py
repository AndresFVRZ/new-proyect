from sqlalchemy import Column, Integer, String, DECIMAL, Date, ForeignKey
from database import Base

# 1. Modelo Marca
class Marca(Base):
    __tablename__ = "marcas"
    
    id_marca = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(50), nullable=False, unique=True)
    pais_origen = Column(String(50))

# 2. Modelo Moto
class Moto(Base):
    __tablename__ = "motos"
    
    id_moto = Column(Integer, primary_key=True, index=True, autoincrement=True)
    modelo = Column(String(50), nullable=False)
    año = Column(Integer)
    cilindraje = Column(Integer)
    precio = Column(DECIMAL(10,2))
    id_marca = Column(Integer, ForeignKey("marcas.id_marca"), nullable=False)

# 3. Modelo Cliente
class Cliente(Base):
    __tablename__ = "clientes"
    
    id_cliente = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    telefono = Column(String(20))
    correo = Column(String(100), unique=True)
    direccion = Column(String(200))

# 4. Modelo Venta
class Venta(Base):
    __tablename__ = "ventas"
    
    id_venta = Column(Integer, primary_key=True, index=True, autoincrement=True)
    fecha_venta = Column(Date, nullable=False)
    id_cliente = Column(Integer, ForeignKey("clientes.id_cliente"), nullable=False)
    total = Column(DECIMAL(10,2))

# 5. Modelo DetalleVenta
class DetalleVenta(Base):
    __tablename__ = "detalle_venta"
    
    id_detalle = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_venta = Column(Integer, ForeignKey("ventas.id_venta"), nullable=False)
    id_moto = Column(Integer, ForeignKey("motos.id_moto"), nullable=False)
    cantidad = Column(Integer, default=1)
    precio_unitario = Column(DECIMAL(10,2), nullable=False)