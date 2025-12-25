# 🪐 NMS Galactic Trade Manager

Aplicación desarrollada en **Python + Streamlit** para la gestión de estaciones comerciales en *No Man’s Sky*.

Permite registrar, consultar y editar estaciones espaciales, sus economías y los bienes que compran y venden, con persistencia local y una interfaz clara orientada a uso práctico.

---

## ✨ Características principales

- CRUD completo de estaciones espaciales
- Gestión centralizada de:
  - Items comerciales
  - Tipos de economía
- Registro de:
  - Productos que la estación vende (tú compras)
  - Productos que la estación compra (tú vendes)
- Filtros de búsqueda por sistema, economía y productos
- Persistencia local mediante archivos JSON
- Arquitectura modular y mantenible

---

## 🧱 Arquitectura del proyecto

El proyecto está estructurado siguiendo buenas prácticas:

- Separación clara entre:
  - UI (Streamlit)
  - Lógica de negocio
  - Persistencia
  - Estado de la aplicación
- Código preparado para:
  - Escalar (SQLite, nuevas vistas, estadísticas)
  - Empaquetarse como ejecutable (`PyInstaller`)
  - Uso local o publicación online

### Requisitos
- Python 3.12.1 instalado y añadido al PATH

### Ejecución rápida (Windows)
Ejecutar:
NMS Trade Manager.bat

### Ejecución CMD
```bash
pip install -r requirements.txt
set PYTHONPATH=.
streamlit run app/main.py