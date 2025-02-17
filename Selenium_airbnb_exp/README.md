# Selenium Web Scraper para Airbnb

Este proyecto utiliza Selenium para automatizar la extracción de datos de experiencias en Airbnb en una comunidad. Luego busca el enlace a Google del mapa de cada página y lo extrae para obtener las coordenadas del punto en el que se localizan las experiencias. 

## 📁 Estructura del Proyecto
selenium/ │── src/ # Código fuente │ ├── airbnb_scraper.py │ ├── extract_location_scroll.py │ ├── airbnb_enlaceexp_google.py │── drivers/ # Webdrivers como ChromeDriver │ ├── chromedriver.exe │── logs/ # Archivos de registro │ ├── network_logs.json │── README.md # Este archivo │── requirements.txt # Librerías necesarias

## 🚀 Instalación y Uso

### 1️⃣ Requisitos previos
- Tener Python instalado (`python --version` para verificar).
- Instalar las dependencias necesarias:
  ```bash
  pip install -r requirements.txt

## Para ejecutar el script:
### Extraer experiencias
python src/airbnb_scraper.py
### Comprobar enlace Google en una experiencia
python src/airbnb_enlaceexp_google.py
### Extraer enlace Google revisando cada experiencia + scroll para que cargue el mapa
python src/extract_location_scroll.py

# 📌 Autor
Beatriz Acero