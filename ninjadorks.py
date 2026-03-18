from dotenv import load_dotenv, set_key
import argparse
import sys
import os

from googlesearch import GoogleSearch

def env_config():
    """Configurar el archivo .env con los valores proporcionados"""
    api_key = input("Introduce tu API_KEY de SerAPI: ")
    set_key(".env", "API_KEY_SERPAPI", api_key)

def main(query, configure_env, start_page, pages, lang):
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

    if not query:
        print("Indica una consulta con el comando -q. Utiliza el comando -h para mostrar la ayuda")
        sys.exit(1)

    gsearch = GoogleSearch(API_KEY_SERPAPI)

    results = gsearch.search(query,
                             start_page=start_page,
                             pages=pages,
                             lang=lang)


    print(results)

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
    args = parser.parse_args()
    main(query=args.query,
         configure_env=args.configure,
         pages=args.pages,
         start_page=args.start_page,
         lang=args.lang)