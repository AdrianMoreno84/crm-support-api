from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from enum import Enum
# Clase que valida que solo sean posibles las 3 opciones 
class ClientStatus(str, Enum):
    PROSPECTO = "Prospecto"
    ACTIVO = "Activo"
    INACTIVO = "Inactivo"
# Clase que valida que solo sean posibles las 3 opciones 
class TicketPriority(str, Enum):
    BAJA = "Baja"
    MEDIA = "Media"
    ALTA = "Alta"
# Clase que valida que solo sean posibles las 3 opciones 
class TicketStatus(str, Enum):
    ABIERTO = "Abierto"
    EN_PROGRESO = "En Progreso"
    CERRADO = "Cerrado"

# --- Esquemas de Ticket ---
#define los campos que el cliente debe enviar al crear el ticket
class TicketCreate(BaseModel):
    title: str
    description: str
    # si no se especifica la prioridad, el sistema le asigna lo que esta en MEDIA
    priority: TicketPriority = TicketPriority.MEDIA
    client_id: int
# define que datos se esperan cuando se va a ctualizar un ticket
class TicketUpdate(BaseModel):
    status: TicketStatus
    resolution: Optional[str] = None
#defrine los campos que devuelve la aplicacion en Json
class TicketResponse(BaseModel):
    id: int
    title: str
    description: str
    priority: str
    status: str
    resolution: Optional[str]
    client_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# --- Esquemas de Client ---
# Valida los datos al crear un cliente
class ClientCreate(BaseModel):
    name: str
    email: EmailStr
    company: str
# Valida los datos que devuelve al consultar un cliente
class ClientResponse(BaseModel):
    id: int
    name: str
    email: str
    company: str
    status: str
    created_at: datetime
    # dada la relacion cliente ticket, devuelve la lista de tickets de un cliente
    tickets: List[TicketResponse] = []
    # permite que pueda leer y extraer desde la base usando notacion de punto.
    class Config:
        from_attributes = True