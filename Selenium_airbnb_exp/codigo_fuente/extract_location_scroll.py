import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

# 📌 Cargar el archivo Excel con las experiencias
file_path = "airbnb_experiences_madrid.xlsx"
df = pd.read_excel(file_path)

# 📌 Inicializar Selenium
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")  # Maximizar la ventana
driver = webdriver.Chrome(options=options)

# 📌 Lista para almacenar las URLs de Google Maps
map_urls = []

for index, row in df.iterrows():
    airbnb_url = row["URL"]
    driver.get(airbnb_url)

    # 📌 Esperar a que la página cargue completamente
    time.sleep(5)  # Ajusta este tiempo si es necesario

    print(f"\n🔍 Revisando: {airbnb_url}")

    try:
        # 📌 Hacer scroll varias veces con PAGE_DOWN para asegurarnos de que el mapa cargue
        body = driver.find_element(By.TAG_NAME, "body")
        for _ in range(5):  # Desplazar 5 veces hacia abajo
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(1)

        # 📌 Intentar ubicar el enlace del mapa en la página
        map_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(@href, 'maps.google.com/maps?')]"))
        )

        # 📌 **Forzar scroll hasta el mapa con JavaScript**
        driver.execute_script("window.scrollTo(0, arguments[0].getBoundingClientRect().top + window.scrollY - 200);", map_element)
        time.sleep(5)  # Esperar a que cargue

        # 📌 Extraer el enlace de Google Maps
        map_link = map_element.get_attribute("href")
        print(f"✅ Enlace de Google Maps encontrado: {map_link}")

    except Exception:
        print(f"❌ No se encontró el enlace de Google Maps en: {airbnb_url}")
        map_link = None

    # Agregar el enlace (o None si no se encontró)
    map_urls.append(map_link)

# 📌 Cerrar Selenium
driver.quit()

# 📌 Agregar la columna con las URLs de Google Maps al DataFrame
df["Google Maps URL"] = map_urls

# 📌 Guardar el nuevo archivo con las URLs de Google Maps añadidas
output_file = "airbnb_experiences_madrid_con_maps.xlsx"
df.to_excel(output_file, index=False)

print(f"\n🎉 Proceso completado. Archivo guardado como: {output_file}")

