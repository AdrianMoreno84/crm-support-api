from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from . import models, schemas

# --- OPERACIONES DE CLIENTES ---
# valida si el cliente existe en la base, si existe arroja error, si no lo crea y lo agrega 
def create_client(db: Session, client: schemas.ClientCreate):
    # Validar que el correo no exista previamente
    existing_client = db.query(models.Client).filter(models.Client.email == client.email).first()
    if existing_client:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un cliente registrado con este correo electrónico."
        )
    
    db_client = models.Client(
        name=client.name,
        email=client.email,
        company=client.company
    )
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client
# devuelve la lista de clientes, con intervelos  y limite  maximos
def get_clients(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Client).offset(skip).limit(limit).all()
# devuelve el cliente determinado por el Id
def get_client_by_id(db: Session, client_id: int):
    client = db.query(models.Client).filter(models.Client.id == client_id).first()
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cliente con ID {client_id} no encontrado."
        )
    return client

# --- OPERACIONES DE TICKETS (CON REGLAS DE NEGOCIO CRM) ---
#crear ticket
def create_ticket(db: Session, ticket: schemas.TicketCreate):
    # 1. Verificar que el cliente exista
    client = get_client_by_id(db, ticket.client_id)

    # 2. Regla de negocio: Si el cliente era 'Prospecto', pasa automáticamente a 'Activo'
    if client.status == "Prospecto":
        client.status = "Activo"

    db_ticket = models.Ticket(
        title=ticket.title,
        description=ticket.description,
        priority=ticket.priority.value,
        client_id=ticket.client_id
    )
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket
# listar tickets por estado y/o por prioridad
def get_tickets(db: Session, status_filter: str = None, priority_filter: str = None):
    query = db.query(models.Ticket)
    if status_filter:
        query = query.filter(models.Ticket.status == status_filter)
    if priority_filter:
        query = query.filter(models.Ticket.priority == priority_filter)
    return query.all()
# actualizar estado del ticket
def update_ticket_status(db: Session, ticket_id: int, ticket_update: schemas.TicketUpdate):
    ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ticket con ID {ticket_id} no encontrado."
        )

    # Regla de negocio: No permitir cerrar un ticket sin documentar la solución
    if ticket_update.status == schemas.TicketStatus.CERRADO:
        # si no hay resolucion, o la longitud de resolucion es menor a 5 envia error
        if not ticket_update.resolution or len(ticket_update.resolution.strip()) < 5:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Para cerrar un ticket debes incluir una resolución detallada (mínimo 5 caracteres)."
            )
        ticket.resolution = ticket_update.resolution

    ticket.status = ticket_update.status.value
    db.commit()
    db.refresh(ticket)
    return ticket