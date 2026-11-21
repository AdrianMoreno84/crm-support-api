from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from . import models, schemas, crud
from .database import engine, get_db

# Crea las tablas en PostgreSQL si no existen
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CRM & Support Ticket API",
    description="API REST para gestión de clientes y casos de soporte técnico con reglas de negocio automatizadas.",
    version="1.0.0"
)
# define la direccion inical del servidor y el mensaje de direccionamiento
@app.get("/", tags=["Health"])
def root():
    return {"message": "CRM Support API operativa. Ve a /docs para probar los endpoints."}

# --- RUTAS DE CLIENTES ---
# define la ruta de creacion de cliente
@app.post("/clients/", response_model=schemas.ClientResponse, status_code=201, tags=["Clients"])
def create_client(client: schemas.ClientCreate, db: Session = Depends(get_db)):
    return crud.create_client(db=db, client=client)
#define la ruta de listar clientes
@app.get("/clients/", response_model=List[schemas.ClientResponse], tags=["Clients"])
def list_clients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_clients(db=db, skip=skip, limit=limit)
#define la ruta de busclar clinetes por Id
@app.get("/clients/{client_id}", response_model=schemas.ClientResponse, tags=["Clients"])
def get_client(client_id: int, db: Session = Depends(get_db)):
    return crud.get_client_by_id(db=db, client_id=client_id)

# --- RUTAS DE TICKETS ---
# define la ruta para crear tickets
@app.post("/tickets/", response_model=schemas.TicketResponse, status_code=201, tags=["Tickets"])
def create_ticket(ticket: schemas.TicketCreate, db: Session = Depends(get_db)):
    return crud.create_ticket(db=db, ticket=ticket)
#define la ruta para obtener el listado de tickets por priridad y/o estado
@app.get("/tickets/", response_model=List[schemas.TicketResponse], tags=["Tickets"])
def list_tickets(
    status: Optional[schemas.TicketStatus] = None,
    priority: Optional[schemas.TicketPriority] = None,
    db: Session = Depends(get_db)
):
    status_val = status.value if status else None
    priority_val = priority.value if priority else None
    return crud.get_tickets(db=db, status_filter=status_val, priority_filter=priority_val)
# define la ruta para la actualizacion de un ticket
@app.patch("/tickets/{ticket_id}", response_model=schemas.TicketResponse, tags=["Tickets"])
def update_ticket(ticket_id: int, ticket_update: schemas.TicketUpdate, db: Session = Depends(get_db)):
    return crud.update_ticket_status(db=db, ticket_id=ticket_id, ticket_update=ticket_update)