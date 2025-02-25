
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Table, DateTime, UniqueConstraint, func
from sqlalchemy.orm import relationship

Base = declarative_base() #Base es la clase base de la que heredan todos los modelos
asociacion_usuarios_reclamos = Table('usuarios_reclamos', Base.metadata,
    Column('user_id', Integer, ForeignKey('usuarios.id')),
    Column('claim_id', Integer, ForeignKey('reclamo.id')),
    UniqueConstraint('user_id', 'claim_id', name='unique_user_claim')  # Restricción de unicidad
)
class ModeloReclamo(Base):
    """Esta clase representa una tabla llamada reclamo en la base de datos:"""
    __tablename__= "reclamo"
    id = Column(Integer(), primary_key=True, autoincrement=True)
    contenido = Column(String(1000),nullable=False)
    clasificacion = Column(String(1000), nullable=False)
    id_usuario = Column(Integer(),ForeignKey('usuarios.id'),nullable=False)
    fecha_de_creacion = Column(DateTime(), nullable=False)
    estado = Column(String(100), nullable=False)
    tiempo_estimado = Column(Integer(), nullable=True)
    tiempo_ocupado = Column(Integer(),nullable=True)
    
    # Relación con el usuario propietario del reclamo (uno-a-muchos)
    usuario = relationship("ModeloUsuario", back_populates="reclamos")

    # Relación muchos-a-muchos con usuarios que siguen el reclamo
    usuarios_seguidores = relationship(
        "ModeloUsuario",
        secondary=asociacion_usuarios_reclamos,
        back_populates="reclamos_seguidos"
    )
        
class ModeloUsuario(Base):
    """Esta clase representa una tabla llamada usuarios en la base de datos:"""
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, autoincrement=True)  # Clave primaria
    nombre = Column(String(1000), nullable=False)
    nombreDeUsuario = Column(String(1000),nullable=False)
    email = Column(String(1000), nullable=False, unique=True)
    claustro = Column(String(1000),nullable=False)
    contraseña = Column(String(1000), nullable=False)
    
    # Relación con reclamos creados por el usuario (uno-a-muchos)
    reclamos = relationship("ModeloReclamo", back_populates="usuario")
    
    # Relación muchos-a-muchos con reclamos seguidos por el usuario
    reclamos_seguidos = relationship(
        "ModeloReclamo",
        secondary=asociacion_usuarios_reclamos,
        back_populates="usuarios_seguidores"
    )
        
    