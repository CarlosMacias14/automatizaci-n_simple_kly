from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.sanitizar import extraer_entidad
from urllib.parse import quote_plus

def obtener_clima(driver, consulta):
    ciudad = extraer_entidad(consulta)
    url = f"https://www.google.com/search?q={quote_plus(f'clima {ciudad}')}&hl=es&gl=mx"
    driver.get(url)

    try:
        espera = WebDriverWait(driver, 5)
        # Extrae ubicacion
        ubicacion = driver.find_element(By.CSS_SELECTOR, "span[class='BBwThe']").text
        # Extraer temperatura de la ubicacion
        temp = driver.find_element(By.CSS_SELECTOR, "#wob_tm").text
        # Extraer si esta despejado o estado del clima
        desc = driver.find_element(By.CSS_SELECTOR, "#wob_dc").text
        # Extraer humedad de la ubicacion
        humedad = driver.find_element(By.CSS_SELECTOR, "#wob_hm").text
        # Resultado del srcaping
        return f"En {ubicacion} hace {temp}°C, esta {desc.lower()}. Humedad: {humedad}."

    except Exception as e:
        print(f"[ERROR DEBUG FATAL] Clima: {e}")
        return f"Error procesando la página del clima para '{ciudad}'."