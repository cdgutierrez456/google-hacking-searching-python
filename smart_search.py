import os
import re
import argparse

class SmartSearch:

    def __init__(self, dir_path):
        self.dir_path = dir_path
        self.files = self._read_files()

    def _read_files(self):
        """Lee el contenido de los fichereos que se encuentran en un directorio"""
        files = {}
        # Listar los ficheros del directorio
        for file in os.listdir(self.dir_path):
            file_path = os.path.join(self.dir_path, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    files[file] = f.read()
            except Exception as e:
                print(f'Error al leer el archivo {file_path}: {e}')

        return files

    def regex_search(self, regex):
        """Busca informacion utilizando expresiones regulares"""
        coincidences = {}
        # Recorremos el contenido de todos los fichereos del directorio
        for file, text in self.files.items():
            respons = ''
            while respons not in ('y', 'yes', 'n', 'no'):
                respons = input(f'El fichero {file} tiene una longitud de {len(text)} caracteres, quieres procesarlo? (y/n): ')
            if respons in ('n', 'no'):
                continue
            matches = re.findall(regex, text, re.IGNORECASE)
            if not matches == []:
                coincidences[file] = matches
        return coincidences

if __name__ == '__main__':
    # Configuramos los argumentos del programa
    parser = argparse.ArgumentParser(description="Esta herramienta realiza busquedas en los ficheros de un directorio")
    parser.add_argument('dir_path', type=str, help='La ruta al directorio donde se encuntran los ficheros')
    parser.add_argument('-r', '--regex', type=str, help='La expresion regular para realizar la busqueda.')

    # Paseamos los argumentos
    args = parser.parse_args()

    if (args.regex):
        searcher = SmartSearch(args.dir_path)
        results = searcher.regex_search(args.regex)
        print()
        for file, res in results.items():
            print(file)
            for r in res:
                print(f'\t- {r}')
        print(results)