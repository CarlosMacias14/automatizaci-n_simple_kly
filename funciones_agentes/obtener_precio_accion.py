from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.sanitizar import extraer_entidad
from urllib.parse import quote_plus
import re

def obtener_precio_accion(driver, consulta):
    empresa = extraer_entidad(consulta)
    url = f"https://www.google.com/search?q={quote_plus(f'precio accion {empresa}')}&hl=es&gl=mx"
    driver.get(url)

    try:
        espera = WebDriverWait(driver, 5)
        # Extrae nombre de empresa
        empresa = driver.find_element(By.CSS_SELECTOR, "div[class='PZPZlf ssJ7i B5dxMb']").text
        # Extrae precio de accion
        precio = driver.find_element(By.CSS_SELECTOR, "span[jsname='L3mUVe']").text
        # Extrae divisa de accion
        divisa = driver.find_element(By.CSS_SELECTOR, "span[jsname='T3Us2d']").text
        # Extrae tikcer de accion, ejemplo Microsoft [BMV: MSFT]
        ticker = driver.find_element(By.CSS_SELECTOR, 'div[class="iAIpCb PZPZlf"]').text
        # Resultado del scraping
        return f"{empresa.title()} [{ticker}] ${precio} {divisa.upper()}"            

    except Exception as e:
        print(f"[ERROR DEBUG FATAL] Acción: {e}")
        return f"Error procesando la página de finanzas para '{empresa}'."
