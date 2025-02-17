from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Configurar Selenium con ChromeDriver
chrome_driver_path = "C:/selenium/chromedriver.exe"  # Ajusta la ruta si es diferente
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Comenta esta línea si quieres ver el navegador
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# URL de experiencias en Madrid
url = "https://www.airbnb.es/s/Madrid--Espa%C3%B1a/experiences?place_id=ChIJuTPgQHqBQQ0RgMhLvvNAAwE&refinement_paths%5B%5D=%2Fexperiences&date_picker_type=calendar&adults=0&children=0&infants=0&pets=0&search_type=AUTOSUGGEST"
driver.get(url)

# Esperar que la página cargue completamente
time.sleep(3)

# Cargar más experiencias haciendo clic en "Carga más"
while True:
    try:
        load_more_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Carga más')]"))
        )
        load_more_button.click()
        print("🔄 Se hizo clic en 'Carga más', cargando más experiencias...")
        time.sleep(3)  # Espera que cargue antes de intentar de nuevo
    except:
        print("✅ No hay más experiencias para cargar.")
        break  # Si no encuentra el botón, significa que ya cargó todas las experiencias

# Esperar unos segundos después de la última carga
time.sleep(2)

# Extraer las experiencias
experiences = []
cards = driver.find_elements(By.XPATH, "//a[@aria-label]")  # Buscar experiencias por su título en aria-label

print(f"🔍 Se encontraron {len(cards)} experiencias en la página.")

for index, card in enumerate(cards):
    try:
        print(f"📌 Extrayendo experiencia {index + 1}...")

        title = card.get_attribute("aria-label")  # Título
        print(f"  ✅ Título: {title}")

        link = card.get_attribute("href")  # Enlace
        print(f"  ✅ URL: {link}")

        parent_div = card.find_element(By.XPATH, "./ancestor::div[1]")  # Buscar el div inmediato superior

        # Intentar extraer el precio
        try:
            price = parent_div.find_element(By.XPATH, ".//span[contains(text(), 'Desde')]").text
        except:
            price = "No disponible"
        print(f"  ✅ Precio: {price}")

        # Intentar extraer la calificación y número de reseñas
        try:
            rating_info = parent_div.find_element(By.XPATH, ".//span[contains(@aria-hidden, 'true')]").text
            rating, reviews = rating_info.split(" (")  # Divide la calificación y el número de reseñas
            reviews = reviews.replace(")", "")  # Eliminar el paréntesis
        except:
            rating = "No disponible"
            reviews = "No disponible"
        print(f"  ✅ Calificación: {rating} ⭐ ({reviews} reseñas)")

        # Intentar extraer la duración
        try:
            duration = parent_div.find_element(By.XPATH, ".//span[contains(text(),'horas') or contains(text(),'hora')]").text
        except:
            duration = "No disponible"
        print(f"  ✅ Duración: {duration}")

        experiences.append({
            "Título": title,
            "Precio": price,
            "Calificación": rating,
            "Número de Reseñas": reviews,
            "Duración": duration,
            "URL": link
        })
    except Exception as e:
        print(f"❌ Error en la experiencia {index + 1}: {e}")
        continue

# Guardar los datos en un archivo Excel
df = pd.DataFrame(experiences)
df.to_excel("airbnb_experiences_madrid.xlsx", index=False)

print("📂 Datos guardados en airbnb_experiences_madrid.xlsx")
driver.quit()

