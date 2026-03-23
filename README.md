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
├── googlesearch.py      # Clase wrapper sobre la API de SerpAPI
├── ninjadorks.py        # Script principal con CLI: ejecuta búsquedas con dorks
├── results_parser.py    # Clase para mostrar y exportar resultados (tabla, JSON, HTML)
├── file_downloader.py   # Clase para descargar archivos encontrados en los resultados
├── ia_agent.py          # Generadores IA (GPT4All y OpenAI) + agente para generar dorks
├── smart_search.py      # Clase para buscar información en ficheros locales con regex
├── html_template.html   # Plantilla HTML para el reporte de resultados
├── requirements.txt     # Dependencias del proyecto
└── .env                 # Variables de entorno (no subir al repo)
```

---

## Requisitos

- Python 3.x
- Cuenta en [SerpAPI](https://serpapi.com/) para obtener una API key
- (Opcional) [GPT4All](https://gpt4all.io/) para usar el agente IA local
- (Opcional) Cuenta en [OpenAI](https://platform.openai.com/) para usar GPT-4o como generador de dorks

### Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## Configuración

Al ejecutar el script por primera vez (sin `.env`) o usando el flag `-c`, se iniciará un asistente interactivo que pedirá la API key y creará el archivo `.env` automáticamente:

```bash
python ninjadorks.py -c
```

También puedes crear el archivo `.env` manualmente:

```env
API_KEY_SERPAPI=tu_clave_aqui
OPENAI_API_KEY=tu_clave_openai  # opcional, solo si usas el generador OpenAI
```

---

## Uso

### Uso básico

```bash
python ninjadorks.py -q 'filetype:sql "MySQL dump" (pass|password|passwd|pwd)'
```

### Argumentos disponibles

| Argumento        | Descripción                                                        |
|------------------|--------------------------------------------------------------------|
| `-q`, `--query`  | Dork o consulta a buscar                                           |
| `-c`, `--configure` | Inicia la configuración interactiva del archivo `.env`          |
| `--start-page`   | Página de inicio de resultados (default: `1`)                      |
| `--pages`        | Número de páginas de resultados a recuperar (default: `1`)         |
| `--lang`         | Código de idioma para los resultados (default: `lang_es`)          |
| `--json`         | Exporta los resultados a un archivo JSON con el nombre indicado    |
| `--html`         | Exporta los resultados a un archivo HTML con el nombre indicado    |
| `--download`     | Descarga archivos de los resultados según extensión (ej: `pdf,sql,csv`) |
| `-gd`, `--generate-dork` | Genera un dork a partir de una descripción en lenguaje natural (usa IA) |

### Ejemplos

```bash
# Búsqueda simple
python ninjadorks.py -q 'inurl:login admin'

# 3 páginas de resultados en inglés
python ninjadorks.py -q 'filetype:pdf confidential' --pages 3 --lang lang_en

# Exportar a JSON y HTML
python ninjadorks.py -q 'site:ejemplo.com inurl:admin' --json resultados.json --html reporte.html

# Empezar desde la página 2
python ninjadorks.py -q 'intitle:"index of" passwd' --start-page 2 --pages 2

# Descargar archivos PDF encontrados en los resultados
python ninjadorks.py -q 'filetype:pdf confidential' --download pdf

# Descargar múltiples tipos de archivo
python ninjadorks.py -q 'site:ejemplo.com' --download 'pdf,sql,csv'

# Generar un dork con IA (te preguntará si usar OpenAI o GPT4All local)
python ninjadorks.py -gd 'Listado de usuarios y contraseñas en ficheros de texto'
```

---

## Módulos

### `GoogleSearch` (googlesearch.py)

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

#### Parámetros de `search()`

| Parámetro    | Tipo  | Default      | Descripción                                      |
|--------------|-------|--------------|--------------------------------------------------|
| `query`      | str   | —            | La consulta o dork a buscar                      |
| `start_page` | int   | `1`          | Página inicial de resultados                     |
| `pages`      | int   | `1`          | Cantidad de páginas a recuperar                  |
| `lang`       | str   | `'lang_es'`  | Idioma de los resultados (`lang_es`, `lang_en`…) |

---

### `FileDownloader` (file_downloader.py)

Clase para descargar automáticamente archivos encontrados en los resultados de búsqueda.

```python
from file_downloader import FileDownloader

fd = FileDownloader('downloads')  # directorio de destino

# Descargar todos los archivos de una lista de URLs
fd.download_file_filter(urls)

# Filtrar por extensión antes de descargar
fd.download_file_filter(urls, file_types=['pdf', 'sql'])
```

| Método                                  | Descripción                                               |
|-----------------------------------------|-----------------------------------------------------------|
| `file_download(url)`                    | Descarga un archivo individual desde una URL              |
| `download_file_filter(urls, file_types)` | Descarga URLs, filtrando opcionalmente por extensión      |

Los archivos se guardan en el directorio `downloads/` (se crea automáticamente si no existe).

---

### `ResultsParser` (results_parser.py)

Clase encargada de mostrar y exportar los resultados de búsqueda.

| Método                    | Descripción                                         |
|---------------------------|-----------------------------------------------------|
| `screen_show()`           | Muestra los resultados en una tabla en la terminal  |
| `json_export(filename)`   | Exporta los resultados a un archivo JSON            |
| `html_export(filename)`   | Exporta los resultados a un archivo HTML estilizado |

---

### `IAAgent` + generadores (ia_agent.py)

Módulo de generación de Google Dorks con IA mediante patrón estrategia. Permite elegir entre un modelo local (GPT4All) o un modelo en la nube (OpenAI GPT-4o).

#### `GPTAllGenerator` — modelo local

No requiere conexión a internet ni API key. El modelo debe estar descargado previamente en el directorio de modelos de GPT4All.

```python
from ia_agent import GPTAllGenerator, IAAgent

generator = GPTAllGenerator()  # usa orca-mini-3b por defecto
agent = IAAgent(generator)

dork = agent.generate_gdork("Listado de usuarios y contraseñas en ficheros de texto")
print(dork)
# filetype:txt "username" "password"
```

| Parámetro    | Tipo | Default                          | Descripción           |
|--------------|------|----------------------------------|-----------------------|
| `model_name` | str  | `'orca-mini-3b-gguf2-q4_0.gguf'` | Modelo GPT4All a usar |

#### `OpenAIGenerator` — modelo en la nube

Requiere `OPENAI_API_KEY` en el archivo `.env`. Usa el modelo `gpt-4o` por defecto.

```python
from ia_agent import OpenAIGenerator, IAAgent

generator = OpenAIGenerator()
agent = IAAgent(generator)

dork = agent.generate_gdork("Páginas de login expuestas en subdominios de empresas")
print(dork)
```

| Parámetro    | Tipo | Default    | Descripción          |
|--------------|------|------------|----------------------|
| `model_name` | str  | `'gpt-4o'` | Modelo OpenAI a usar |

#### `IAAgent`

Clase agnóstica al generador. Recibe cualquier generador y construye el prompt para generar el dork.

```python
agent = IAAgent(generator)
dork = agent.generate_gdork("descripción en lenguaje natural")
```

---

### `SmartSearch` (smart_search.py)

Herramienta para buscar información en ficheros de texto de un directorio local usando **expresiones regulares**. Útil para analizar volcados de datos o logs obtenidos en una fase de reconocimiento.

```python
from smart_search import SmartSearch

searcher = SmartSearch('/ruta/al/directorio')
results = searcher.regex_search(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+')

for file, matches in results.items():
    print(file, matches)
```

Antes de procesar cada fichero, el script pregunta interactivamente si se desea incluirlo (mostrando su tamaño en caracteres).

#### Uso desde la CLI

```bash
python smart_search.py /ruta/al/directorio -r 'expresion_regular'
```

| Argumento        | Descripción                                      |
|------------------|--------------------------------------------------|
| `dir_path`       | Ruta al directorio con los ficheros a analizar   |
| `-r`, `--regex`  | Expresión regular para realizar la búsqueda      |

---

## Disclaimer

Este proyecto forma parte de un curso de **ethical hacking** con Python. Toda técnica aquí demostrada debe aplicarse únicamente en:

- Entornos de laboratorio propios
- Sistemas con autorización escrita del propietario
- Plataformas de práctica (HackTheBox, TryHackMe, etc.)
