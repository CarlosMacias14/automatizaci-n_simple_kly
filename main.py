import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Funciones y utilidades
from utils.sanitizar import sanitizar
from funciones_agente.obtener_precio_accion import obtener_precio_accion
from funciones_agente.obtener_clima import obtener_clima

def configurar_driver():
    """Configuracion e inicializacion el WebDriver de Selenium con evasión de bots."""
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    # ANTI-DETECCIÓN
    # Esto quita el banner de "Chrome is being controlled..."
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--disable-blink-features=AutomationControlled')
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    # Inyectamos un script para borrar la huella de "webdriver" del navegador
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
        'source': '''
            Object.defineProperty(navigator, 'webdriver', {
              get: () => undefined
            })
        '''
    })
    
    return driver

def procesar_input(user_input_sanitizado):
    """Determina qué función de agente debe ejecutarse según el input."""
    if "clima" in user_input_sanitizado or "temperatura" in user_input_sanitizado:
        return obtener_clima
    
    if any(palabra in user_input_sanitizado for palabra in ["precio", "accion", "valor"]):
        return obtener_precio_accion
        
    return None

def iniciar_asistente():
    print("Iniciando navegador... por favor espera.")
    driver = configurar_driver()
    
    print("\n¡Hola! Soy tu asistente virtual. Como puedo ayudarte el dia de hoy?.")
    print("Puedo decirte el clima de una ciudad o el precio de una acción.")
    print("(Si deseas terminnar mi programa escribe 'adios' para terminar)\n")

    try:
        while True:
            # 1. Captura y Sanitización inicial (quita acentos y caracteres raros)
            raw_input = input("---> ")
            user_input = sanitizar(raw_input)

            if user_input in ["salir", "adios", "fuera", "adios"]:
                print("Finalizando programa. ¡Hasta luego!")
                break

            # 2. Identificación de la intención
            funcion_agente = procesar_input(user_input)

            # 3. Ejecución
            if funcion_agente:
                print("Buscando información...")
                respuesta = funcion_agente(driver, user_input)
                print(f">>> {respuesta}\n")
            else:
                print("No entendí tu solicitud. Prueba con algo como 'clima en Madrid' o 'precio de Apple'.\n")

    except KeyboardInterrupt:
        print("\nPrograma interrumpido por el usuario.")
    finally:
        # Cerramos el navegador siempre, sin importar que
        driver.quit()

if __name__ == "__main__":
    iniciar_asistente()
