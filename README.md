# 01 - Hacking & Searching con Google Dorks

Módulo de reconocimiento pasivo usando la API de Google (SerpAPI) para automatizar búsquedas avanzadas con **Google Dorks**.

## ¿Qué es un Google Dork?

Un Google Dork es una consulta avanzada de búsqueda que utiliza operadores especiales de Google para encontrar información específica expuesta públicamente en internet. Se usan en pentesting para la fase de **reconocimiento (OSINT)**.

Ejemplos de operadores:
- `filetype:sql` — busca archivos de tipo SQL indexados
- `"MySQL dump"` — busca esa frase exacta
- `inurl:admin` — busca URLs que contengan "admin"
- `site:ejemplo.com` — limita la búsqueda a un dominio

> **Importante:** Este proyecto es exclusivamente para uso educativo y pruebas en entornos autorizados. El uso de estas técnicas contra sistemas sin permiso es ilegal.

---

## Estructura del proyecto

```
01-hacking-searching/
├── googlesearch.py     # Clase wrapper sobre la API de SerpAPI
├── ninjadorks.py       # Script principal: ejecuta búsquedas con dorks
├── requirements.txt    # Dependencias del proyecto
└── .env                # Variables de entorno (no subir al repo)
```

---

## Requisitos

- Python 3.x
- Cuenta en [SerpAPI](https://serpapi.com/) para obtener una API key

### Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## Configuración

Crea un archivo `.env` en la raíz del proyecto con tu clave de SerpAPI:

```env
API_KEY_SERPAPI=tu_clave_aqui
```

---

## Uso

### Clase `GoogleSearch` (googlesearch.py)

Wrapper que conecta con SerpAPI y permite paginar resultados.

```python
from googlesearch import GoogleSearch

gs = GoogleSearch("tu_api_key")

# Búsqueda simple
results = gs.search("filetype:pdf confidential")

# Con paginación: página 2, 3 páginas de resultados, en inglés
results = gs.search("inurl:login admin", start_page=2, pages=3, lang="lang_en")
```

Cada resultado devuelto es un diccionario con:
```python
{
    "title": "Título del resultado",
    "description": "Fragmento de texto (snippet)",
    "link": "https://url-del-resultado.com"
}
```

### Script `ninjadorks.py`

Ejecuta un dork de ejemplo que busca volcados de bases de datos MySQL expuestos públicamente:

```bash
python ninjadorks.py
```

El dork utilizado es:
```
filetype:sql "MySQL dump" (pass|password|passwd|pwd)
```

---

## Parámetros de `search()`

| Parámetro    | Tipo  | Default      | Descripción                                      |
|--------------|-------|--------------|--------------------------------------------------|
| `query`      | str   | —            | La consulta o dork a buscar                      |
| `start_page` | int   | `1`          | Página inicial de resultados                     |
| `pages`      | int   | `1`          | Cantidad de páginas a recuperar                  |
| `lang`       | str   | `'lang_es'`  | Idioma de los resultados (`lang_es`, `lang_en`…) |

---

## Disclaimer

Este proyecto forma parte de un curso de **ethical hacking** con Python. Toda técnica aquí demostrada debe aplicarse únicamente en:

- Entornos de laboratorio propios
- Sistemas con autorización escrita del propietario
- Plataformas de práctica (HackTheBox, TryHackMe, etc.)
