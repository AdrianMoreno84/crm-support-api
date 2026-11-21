from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from .database import Base
# crear la clase Client que hereda de Base
class Client(Base):
    #nombra la tabla
    __tablename__ = "clients"
    #crea las columnas o campos con sus caracteristicas
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, index=True, nullable=False)
    company = Column(String(100), nullable=False)
    status = Column(String(20), default="Prospecto")  # Prospecto, Activo, Inactivo
    # guarda la fecha de creacion del registro
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relación 1 a muchos con Ticket
    tickets = relationship("Ticket", back_populates="client", cascade="all, delete-orphan")

#crea clase Ticket
class Ticket(Base):
    #nombra tabla
    __tablename__ = "tickets"
    #crea las columnas o campos con sus caracteristicas
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), nullable=False)
    description = Column(Text, nullable=False)
    priority = Column(String(20), default="Media")    # Baja, Media, Alta
    status = Column(String(20), default="Abierto")    # Abierto, En Progreso, Cerrado
    resolution = Column(Text, nullable=True)          # Obligatorio al cerrar el ticket
    # guarda la fecha de creacion del registro
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Llave foránea hacia Client
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    client = relationship("Client", back_populates="tickets")