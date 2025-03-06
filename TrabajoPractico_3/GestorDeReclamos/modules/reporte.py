
import fpdf
from modules.clasesAbstractas import ReporteAbstracto
    
class ReportePDF(ReporteAbstracto):
    def __init__(self):
        pass
    
    def generarArchivo(self,ruta_documento:str,ruta_imagen:str):
        """
        Genera un archivo PDF que incluye las imágenes generadas.
        
        :param ruta_imagen: Ruta de la imagen a incluir en el PDF (formato JPG, PNG, etc.).
        :param ruta_documento: Ruta del archivo PDF a generar.
        """
        pdf = fpdf.FPDF(orientation='P', unit='mm', format='A4')
        pdf.add_page()
        pdf.image(ruta_imagen, type='JPG', x=10, y=40, w=190)  
        pdf.output(ruta_documento)
        

class ReporteHTML(ReporteAbstracto):
    def __init__(self):
        pass
             
    def generarArchivo(self,ruta_documento:str,ruta_imagen:str):
        """
        Genera un archivo HTML que incluye las imágenes generadas.
        
        :param ruta_imagen: Ruta de la imagen a incluir en el HTML (formato JPG, PNG, etc.).
        :param ruta_documento: Ruta del archivo HTML a generar.
        """
        ruta_img = "D:/Documentos D/Facultad/ProgAvanzadaPython/Práctica/BenitezGonzaloFinalProgAvanzada/TrabajoPractico_3/GestorDeReclamos/"+f"{ruta_imagen}"
        # Estructura básica del HTML
        contenido_html = f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Reporte Gráfico</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 20px;
                }}
                img {{
                    max-width: 100%;
                    height: auto;
                    margin: 20px 0;
                }}
            </style>
        </head>
        <body>
            <h1>Reporte Gráfico</h1>
            <p>A continuación, se muestran las gráficas generadas:</p>
            <img src="{ruta_img}" alt="Gráfico WordCloud y Torta">
        </body>
        </html>
        """

        # Guardar el contenido en un archivo HTML
        with open(ruta_documento, "w", encoding="utf-8") as archivo:
            archivo.write(contenido_html)