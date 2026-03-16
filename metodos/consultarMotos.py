from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List
from datetime import date

from database import get_db
from modelos import model_motos as models
from esquemas import eschemas_motos as schemas

router = APIRouter()

# ==================== MARCAS ====================
@router.get("/marcas", response_model=List[schemas.Marca])
def get_marcas(db: Session = Depends(get_db)):
    return db.query(models.Marca).all()

@router.get("/marcas/{id_marca}", response_model=schemas.Marca)
def get_marca(id_marca: int, db: Session = Depends(get_db)):
    marca = db.query(models.Marca).filter(models.Marca.id_marca == id_marca).first()
    if not marca:
        raise HTTPException(status_code=404, detail="Marca no encontrada")
    return marca

@router.post("/marcas", response_model=schemas.Marca, status_code=status.HTTP_201_CREATED)
def create_marca(marca: schemas.MarcaCreate, db: Session = Depends(get_db)):
    db_marca = models.Marca(**marca.model_dump())
    db.add(db_marca)
    db.commit()
    db.refresh(db_marca)
    return db_marca

@router.put("/marcas/{id_marca}", response_model=schemas.Marca)
def update_marca(id_marca: int, marca: schemas.MarcaCreate, db: Session = Depends(get_db)):
    db_marca = db.query(models.Marca).filter(models.Marca.id_marca == id_marca).first()
    if not db_marca:
        raise HTTPException(status_code=404, detail="Marca no encontrada")
    
    for key, value in marca.model_dump().items():
        setattr(db_marca, key, value)
    
    db.commit()
    db.refresh(db_marca)
    return db_marca

@router.delete("/marcas/{id_marca}")
def delete_marca(id_marca: int, db: Session = Depends(get_db)):
    db_marca = db.query(models.Marca).filter(models.Marca.id_marca == id_marca).first()
    if not db_marca:
        raise HTTPException(status_code=404, detail="Marca no encontrada")
    
    db.delete(db_marca)
    db.commit()
    return {"detail": "Marca eliminada"}

# ==================== MOTOS ====================
@router.get("/motos", response_model=List[schemas.Moto])
def get_motos(db: Session = Depends(get_db)):
    return db.query(models.Moto).all()

@router.get("/motos/con-marca", response_model=List[schemas.MotoConMarca])
def get_motos_con_marca(db: Session = Depends(get_db)):
    return db.query(models.Moto).options(joinedload(models.Moto.marca)).all()

@router.get("/motos/{id_moto}", response_model=schemas.Moto)
def get_moto(id_moto: int, db: Session = Depends(get_db)):
    moto = db.query(models.Moto).filter(models.Moto.id_moto == id_moto).first()
    if not moto:
        raise HTTPException(status_code=404, detail="Moto no encontrada")
    return moto

@router.get("/motos/{id_moto}/con-marca", response_model=schemas.MotoConMarca)
def get_moto_con_marca(id_moto: int, db: Session = Depends(get_db)):
    moto = db.query(models.Moto).options(
        joinedload(models.Moto.marca)
    ).filter(models.Moto.id_moto == id_moto).first()
    
    if not moto:
        raise HTTPException(status_code=404, detail="Moto no encontrada")
    return moto

@router.get("/marcas/{id_marca}/motos", response_model=List[schemas.Moto])
def get_motos_por_marca(id_marca: int, db: Session = Depends(get_db)):
    return db.query(models.Moto).filter(models.Moto.id_marca == id_marca).all()

@router.post("/motos", response_model=schemas.Moto, status_code=status.HTTP_201_CREATED)
def create_moto(moto: schemas.MotoCreate, db: Session = Depends(get_db)):
    # Verificar que la marca existe
    marca = db.query(models.Marca).filter(models.Marca.id_marca == moto.id_marca).first()
    if not marca:
        raise HTTPException(status_code=400, detail="La marca especificada no existe")
    
    db_moto = models.Moto(**moto.model_dump())
    db.add(db_moto)
    db.commit()
    db.refresh(db_moto)
    return db_moto

@router.put("/motos/{id_moto}", response_model=schemas.Moto)
def update_moto(id_moto: int, moto: schemas.MotoCreate, db: Session = Depends(get_db)):
    db_moto = db.query(models.Moto).filter(models.Moto.id_moto == id_moto).first()
    if not db_moto:
        raise HTTPException(status_code=404, detail="Moto no encontrada")
    
    for key, value in moto.model_dump().items():
        setattr(db_moto, key, value)
    
    db.commit()
    db.refresh(db_moto)
    return db_moto

@router.delete("/motos/{id_moto}")
def delete_moto(id_moto: int, db: Session = Depends(get_db)):
    db_moto = db.query(models.Moto).filter(models.Moto.id_moto == id_moto).first()
    if not db_moto:
        raise HTTPException(status_code=404, detail="Moto no encontrada")
    
    db.delete(db_moto)
    db.commit()
    return {"detail": "Moto eliminada"}

# ==================== CLIENTES ====================
@router.get("/clientes", response_model=List[schemas.Cliente])
def get_clientes(db: Session = Depends(get_db)):
    return db.query(models.Cliente).all()

@router.get("/clientes/{id_cliente}", response_model=schemas.Cliente)
def get_cliente(id_cliente: int, db: Session = Depends(get_db)):
    cliente = db.query(models.Cliente).filter(models.Cliente.id_cliente == id_cliente).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente

@router.post("/clientes", response_model=schemas.Cliente, status_code=status.HTTP_201_CREATED)
def create_cliente(cliente: schemas.ClienteCreate, db: Session = Depends(get_db)):
    # Verificar si el correo ya existe
    existe = db.query(models.Cliente).filter(models.Cliente.correo == cliente.correo).first()
    if existe:
        raise HTTPException(status_code=400, detail="Ya existe un cliente con ese correo")
    
    db_cliente = models.Cliente(**cliente.model_dump())
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

@router.put("/clientes/{id_cliente}", response_model=schemas.Cliente)
def update_cliente(id_cliente: int, cliente: schemas.ClienteCreate, db: Session = Depends(get_db)):
    db_cliente = db.query(models.Cliente).filter(models.Cliente.id_cliente == id_cliente).first()
    if not db_cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    for key, value in cliente.model_dump().items():
        setattr(db_cliente, key, value)
    
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

@router.delete("/clientes/{id_cliente}")
def delete_cliente(id_cliente: int, db: Session = Depends(get_db)):
    db_cliente = db.query(models.Cliente).filter(models.Cliente.id_cliente == id_cliente).first()
    if not db_cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    db.delete(db_cliente)
    db.commit()
    return {"detail": "Cliente eliminado"}

# ==================== VENTAS ====================
@router.get("/ventas", response_model=List[schemas.Venta])
def get_ventas(db: Session = Depends(get_db)):
    return db.query(models.Venta).all()

@router.get("/ventas/completas", response_model=List[schemas.VentaCompleta])
def get_ventas_completas(db: Session = Depends(get_db)):
    return db.query(models.Venta).options(
        joinedload(models.Venta.cliente),
        joinedload(models.Venta.detalles)
    ).all()

@router.get("/ventas/{id_venta}", response_model=schemas.Venta)
def get_venta(id_venta: int, db: Session = Depends(get_db)):
    venta = db.query(models.Venta).filter(models.Venta.id_venta == id_venta).first()
    if not venta:
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    return venta

@router.get("/ventas/{id_venta}/completa", response_model=schemas.VentaCompleta)
def get_venta_completa(id_venta: int, db: Session = Depends(get_db)):
    venta = db.query(models.Venta).options(
        joinedload(models.Venta.cliente),
        joinedload(models.Venta.detalles)
    ).filter(models.Venta.id_venta == id_venta).first()
    
    if not venta:
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    return venta

@router.get("/clientes/{id_cliente}/ventas", response_model=List[schemas.Venta])
def get_ventas_por_cliente(id_cliente: int, db: Session = Depends(get_db)):
    return db.query(models.Venta).filter(models.Venta.id_cliente == id_cliente).all()

@router.post("/ventas", response_model=schemas.Venta, status_code=status.HTTP_201_CREATED)
def create_venta(venta: schemas.VentaCreate, db: Session = Depends(get_db)):
    # Verificar que el cliente existe
    cliente = db.query(models.Cliente).filter(models.Cliente.id_cliente == venta.id_cliente).first()
    if not cliente:
        raise HTTPException(status_code=400, detail="Cliente no existe")
    
    db_venta = models.Venta(**venta.model_dump())
    db.add(db_venta)
    db.commit()
    db.refresh(db_venta)
    return db_venta

# ==================== DETALLE VENTA ====================
@router.get("/detalles", response_model=List[schemas.DetalleVenta])
def get_detalles(db: Session = Depends(get_db)):
    return db.query(models.DetalleVenta).all()

@router.get("/ventas/{id_venta}/detalles", response_model=List[schemas.DetalleVenta])
def get_detalles_por_venta(id_venta: int, db: Session = Depends(get_db)):
    return db.query(models.DetalleVenta).filter(models.DetalleVenta.id_venta == id_venta).all()

@router.post("/detalles", response_model=schemas.DetalleVenta, status_code=status.HTTP_201_CREATED)
def create_detalle(detalle: schemas.DetalleVentaCreate, db: Session = Depends(get_db)):
    # Verificar que la venta existe
    venta = db.query(models.Venta).filter(models.Venta.id_venta == detalle.id_venta).first()
    if not venta:
        raise HTTPException(status_code=400, detail="Venta no existe")
    
    # Verificar que la moto existe
    moto = db.query(models.Moto).filter(models.Moto.id_moto == detalle.id_moto).first()
    if not moto:
        raise HTTPException(status_code=400, detail="Moto no existe")
    
    # Crear detalle
    db_detalle = models.DetalleVenta(**detalle.model_dump())
    db.add(db_detalle)
    
    # Actualizar total de la venta
    subtotal = detalle.cantidad * detalle.precio_unitario
    venta.total = (venta.total or 0) + subtotal
    
    db.commit()
    db.refresh(db_detalle)
    return db_detalle

@router.delete("/detalles/{id_detalle}")
def delete_detalle(id_detalle: int, db: Session = Depends(get_db)):
    db_detalle = db.query(models.DetalleVenta).filter(models.DetalleVenta.id_detalle == id_detalle).first()
    if not db_detalle:
        raise HTTPException(status_code=404, detail="Detalle no encontrado")
    
    # Actualizar total de la venta
    venta = db.query(models.Venta).filter(models.Venta.id_venta == db_detalle.id_venta).first()
    if venta:
        subtotal = db_detalle.cantidad * db_detalle.precio_unitario
        venta.total = venta.total - subtotal
    
    db.delete(db_detalle)
    db.commit()
    return {"detail": "Detalle eliminado"}