from modules.persistencia import RepositorioUsuariosSQLAlchemy, RepositorioReclamosSQLAlchemy
from modules.reporte import ReportePDF,ReporteHTML
from modules.config import crear_engine

def crear_repositorio():
    session = crear_engine()
    repo_reclamo =  RepositorioReclamosSQLAlchemy(session())
    repo_usuario = RepositorioUsuariosSQLAlchemy(session())
    return repo_reclamo,repo_usuario

def crear_reportes():
    repoPDF = ReportePDF()
    repoHTML = ReporteHTML()
    return repoPDF,repoHTML
    
