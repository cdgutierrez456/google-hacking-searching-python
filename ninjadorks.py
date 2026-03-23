from dotenv import load_dotenv, set_key
from results_parser import ResultsParser
from file_downloader import FileDownloader
from ia_agent import OpenAIGenerator, GPTAllGenerator, IAAgent
import argparse
import sys
import os

from googlesearch import GoogleSearch

def env_config():
    """Configurar el archivo .env con los valores proporcionados"""
    api_key = input("Introduce tu API_KEY de SerAPI: ")
    set_key(".env", "API_KEY_SERPAPI", api_key)

def openai_config():
    """Configura la API KEY de OpenAI en el fichero .env"""
    api_key = input('Introduce la API KEY de OpenAI: ')
    set_key('.env', 'OPENAI_API_KEY', api_key)

def main(query, configure_env, start_page, pages, lang, output_json, output_html, download, gen_dork):
    # Comprobamos si existe el fichero .env
    env_exist = os.path.exists(".env")
    if not env_exist or configure_env:
        env_config()
        print("Archivo .env configurado satisfactoriamente")
        sys.exit(1)

    # Cargamos las variables en el entorno
    load_dotenv()

    # Leemos la clave API
    API_KEY_SERPAPI = os.getenv('API_KEY_SERPAPI')

    if gen_dork:
        # Preguntamos si el usuario quiere utilizar un modelo local u OpenAi
        respons = ''
        while respons.lower() not in ('y', 'yes', 'no', 'n'):
            respons = input('Quieres utilizar GPT-4 de OpenAI (yes/no)?: ')

        if respons.lower() in ('y', 'yes'):
            # Comprobamos si esta definida la API KEY de OpenAI en el fichero .env
            if not 'OPENAI_API_KEY' in os.environ:
                openai_config()
                load_dotenv()

            # Generamos el dork
            openai_generator = OpenAIGenerator()
            ia_agent = IAAgent(openai_generator)
        else:
            print('Utilizando gpt4all y ejecutando la generacion en local. Puede tardar varios minutos...')
            gpt4all_generator = GPTAllGenerator()
            ia_agent = IAAgent(gpt4all_generator)

        result = ia_agent.generate_gdork(gen_dork)
        print(f'\nResultado:\n{result}')
        sys.exit(1)

    if not query:
        print("Indica una consulta con el comando -q. Utiliza el comando -h para mostrar la ayuda")
        sys.exit(1)

    gsearch = GoogleSearch(API_KEY_SERPAPI)

    results = gsearch.search(query,
                             start_page=start_page,
                             pages=pages,
                             lang=lang)


    rparser = ResultsParser(results)
    # Mostrar por console

    rparser.screen_show()

    if output_html:
        rparser.html_export(output_html)

    if output_json:
        rparser.json_export(output_json)

    if download:
        # Separar las extensiones de los archivos en un alista
        file_types = download.split(',')
        # Nos quedamos con las urls de los resultados obtenidos
        urls = [result['link'] for result in results]
        fdownloader = FileDownloader('downloads')
        fdownloader.download_file_filter(urls, file_types)

if __name__ == "__main__":
    # Configuracion de los argumentos del programa
    parser = argparse.ArgumentParser(description="Esta herramienta premite realizar Hacking con buscadores de manera automatica.")
    parser.add_argument("-q", "--query", type=str,
                        help="Especifica el dork que dessea buscar \nEjemplo: -q 'filetype:sql \"MySQL dump\" (pass|password|passwd|pwd)'")
    parser.add_argument("-c", "--configure", action="store_true",
                        help="Incia el proceso de configuracion del archivo .env.\nUtiliza esta opcion sin otros argumentos para configurar las claves.")
    parser.add_argument("--start-page", type=int, default=1,
                        help="Define la pagina de inicio del buscador para obtener los resultados")
    parser.add_argument("--pages", type=int, default=1,
                        help="Numero de paginas de resultados de busqueda.")
    parser.add_argument("--lang", type=str, default="lang_es",
                        help="Codigo de idioma para los resultados de busqueda. Por defecto es 'lang_es'")
    parser.add_argument("--json", type=str,
                        help="Exporta los resultados en formato JSON en el fichero especificado")
    parser.add_argument("--html", type=str,
                        help="Exporta los resultados en formato HTML en el fichero especificado")
    parser.add_argument("--download", type=str,
                        help="Especifica las extensiones de los archivos que quieres descargar separadas entre coma. Ej. --download 'pdf, sql, csv'")
    parser.add_argument("-gd", "--generate-dork", type=str,
                        help="Genera un dork a partir de una descripcion proporcionada por el usuario.\nEj: --generate-dork 'Listado de usuarios y passwords en ficheros de texto'")

    args = parser.parse_args()
    main(query=args.query,
         configure_env=args.configure,
         pages=args.pages,
         start_page=args.start_page,
         lang=args.lang,
         output_json=args.json,
         output_html=args.html,
         download=args.download,
         gen_dork=args.generate_dork)