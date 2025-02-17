import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Configurar el driver de Chrome
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Opcional: Ejecuta el navegador en segundo plano
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# URL de la página donde está el enlace de Google Maps (cámbiala por la real)
URL = "URL"
driver.get(URL)

try:
    # 🔹 Encuentra el enlace de Google Maps en la página
    map_link_element = driver.find_element(By.XPATH, "//a[contains(@href, 'maps.google.com/maps?ll=')]")
    map_link = map_link_element.get_attribute("href")

    # 🔥 VERIFICACIÓN: Imprime el enlace extraído para asegurarnos de que Selenium lo obtiene
    print(f"✅ Enlace de Google Maps extraído: {map_link}")  

    # 🔹 Intentar extraer coordenadas con regex
    match = re.search(r"ll=([-.\d]+),([-.\d]+)", map_link)
    if match:
        lat, lon = match.groups()
        print(f"📍 Coordenadas extraídas correctamente: {lat}, {lon}")
    else:
        lat, lon = "No disponible", "No disponible"
        print("⚠️ No se pudieron extraer las coordenadas.")

except Exception as e:
    print(f"⚠️ No se encontró el enlace de Google Maps. Error: {e}")
    lat, lon = "No disponible", "No disponible"

# Cerrar el navegador
driver.quit()

# 📌 Devolver coordenadas extraídas
print(f"📍 Coordenadas finales: {lat}, {lon}")


