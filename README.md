# 🐍 Proyecto Ouroboros: PoC de Pipeline DevSecOps

![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Framework-Flask-green?logo=flask&logoColor=white)
![Security](https://img.shields.io/badge/Security-Snyk-8025be?logo=snyk&logoColor=white)
![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-2088FF?logo=github-actions&logoColor=white)

## 📜 Resumen

**Ouroboros** es una Prueba de Concepto (PoC) diseñada para demostrar la integración de controles de seguridad automatizados dentro de un pipeline CI/CD.

El objetivo fue simular un escenario real donde código "impuro" (vulnerable) llega al repositorio, es detectado por un guardián automatizado (**Snyk**) y posteriormente refactorizado ("transmutado") a un estado seguro antes del despliegue.

## 🧪 El Experimento

El repositorio comenzó con una aplicación Flask diseñada intencionalmente con fallos comunes del OWASP Top 10.

### 🔴 Fase 1: Estado Vulnerable (La Materia Prima)
El código inicial (`app.py`) incluía:
* **Command Injection:** Entrada de usuario sin sanear directa a `os.popen`.
* **Insecure Deserialization:** Uso de `pickle` con datos no confiables (Riesgo de RCE).
* **XSS Reflected:** Retorno de la salida bruta de comandos al navegador.
* **Dependencias Vulnerables:** Versiones obsoletas de `Flask` y `Requests`.

### 🟢 Fase 2: Estado Transmutado (El Oro)
A través del **pipeline DevSecOps**, el código fue analizado y endurecido (hardening):
* **Validación de Input:** Verificación estricta de tipos usando la librería `ipaddress`.
* **Ejecución Segura:** Reemplazo de la ejecución en shell por `subprocess.run` (listas de argumentos).
* **Serialización Segura:** Reemplazo de `pickle` por `JSON`.
* **Codificación de Salida:** Estandarización de respuestas en `JSON` para mitigar XSS.
* **Gestión de Dependencias:** Actualización de todas las librerías a versiones seguras.

## 🛠️ Arquitectura

1.  **Código:** Python (Flask).
2.  **SCA (Software Composition Analysis):** Snyk Open Source (Analiza `requirements.txt`).
3.  **SAST (Static Application Security Testing):** Snyk Code (Analiza `app.py`).
4.  **Orquestación:** GitHub Actions dispara los escaneos en cada Pull Request.

## 🚀 Cómo ejecutar (Localmente)

Si deseas probar la versión segura de la API:

```bash
# 1. Clonar el repositorio
git clone [https://github.com/Fennek115/Ouroboros-proyect.git](https://github.com/Fennek115/Ouroboros-proyect.git)
cd Ouroboros-proyect

# 2. Crear entorno virtual
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Correr la aplicación
python3 app.py
