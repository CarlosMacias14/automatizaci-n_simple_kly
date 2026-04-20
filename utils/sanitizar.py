# utils/sanitizar.py
import unicodedata
import re

# Lista centralizada y ampliada de palabras que no aportan valor a la búsqueda
PALABRAS_RUIDO = {
    "clima", "temperatura", "precio", "accion", "valor", "de", "del", 
    "la", "el", "una", "un", "por", "favor", "dime", "cual", "es",
    "en", "para", "dame" # He añadido más palabras comunes
}

def sanitizar(texto_usuario):
    """Limpia caracteres, acentos y signos de puntuación."""
    if not texto_usuario:
        return ""
    # Minúsculas y quitar espacios extremos
    texto = texto_usuario.lower().strip()
    # Quitar acentos
    texto = unicodedata.normalize('NFKD', texto).encode('ascii', 'ignore').decode('utf-8')
    # Quitar signos de puntuación (solo deja letras, números y espacios)
    texto = re.sub(r'[^\w\s]', '', texto)
    return texto

def extraer_entidad(consulta_sanitizada):
    """Elimina palabras ruido para dejar solo el nombre de la empresa o ciudad."""
    tokens = consulta_sanitizada.split()
    filtrados = [t for t in tokens if t not in PALABRAS_RUIDO]
    
    # Si al filtrar queda vacío (ej. el usuario solo dijo "clima"), devolvemos la consulta original
    return " ".join(filtrados) if filtrados else consulta_sanitizada