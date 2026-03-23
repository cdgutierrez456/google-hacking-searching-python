import os
import re
import argparse
from transformers import GPT2Tokenizer
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

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

    def ia_search(self, prompt, model_name='gpt-3.5-turbo-0125', max_tokens=100):
        """Realiza busquedas en ficheros con IA"""
        coincidences = {}
        for file, text in self.files.items():
            response = ""
            tokens, cost = self._cost_calculate(text, prompt, model_name, max_tokens)
            while response not in ('y', 'yes', 'n', 'no'):
                response = input(f'El fichero {file} tiene una longitud de {tokens} tokens (aprox. {cost}$). Quieres continuar? (yes/no)')

            if response in ('n', 'no'):
                continue

            # Dividimos el fichero en segmentos
            file_segments = self._split_file(text, model_name)

            # Incializamos el cliente de OpenAI
            client = OpenAI()
            segment_results = []

            for index, segment in enumerate(file_segments):
                print(f'Procesando el segmento {index + 1}/{len(file_segments)}...')
                chat_completion = client.chat.completions.create(
                    messages = [
                        {
                            "role": "user",
                            "content": f"{prompt}\n\nTexto:\n{segment}"
                        }
                    ],
                    model=model_name,
                    max_tokens=max_tokens,
                    n=1
                )
                segment_results.append(chat_completion.choices[0].message.content)

            coincidences[file] = segment_results
        return coincidences


    def _split_file(self, file_text, model_name):
        """Divide el contenido del fichero en segmentos"""
        context_window_sizes = {
            "gpt-4-0125-preview": 128000,
            "gpt-4-1106-preview": 128000,
            "gpt-4": 16000,
            "gpt-4-32k": 32000,
            "gpt-3.5-turbo-0125": 16000,
            "gpt-3.5-turbo-instruct": 4000
        }
        return [file_text[i:i+context_window_sizes[model_name]]
                for i in range(0, len(file_text), context_window_sizes[model_name])]


    def _cost_calculate(self, text, prompt, model_name, max_tokens):
        """Calcula el coste para un modelo de OpenIA"""
        prices = {
            "gpt-4-0125-preview": {"input_cost": 0.01, "output_cost": 0.03},
            "gpt-4-1106-preview": {"input_cost": 0.01, "output_cost": 0.03},
            "gpt-4-1106-vision-preview": {"input_cost": 0.01, "output_cost": 0.03},
            "gpt-4": {"input_cost": 0.03, "output_cost": 0.06},
            "gpt-4-32k": {"input_cost": 0.06, "output_cost": 0.12},
            "gpt-3.5-turbo-0125": {"input_cost": 0.0005, "output_cost": 0.0015},
            "gpt-3.5-turbo-instruct": {"input_cost": 0.0015, "output_cost": 0.002}
        }
        # Tokenizamos el texto perteneciente al archivo
        tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
        len_tokens_prompt = len(tokenizer.tokenize(prompt))
        len_tokens_text = len(tokenizer.tokenize(text))
        # Calculamos el coste de la prediccion
        input_cost = ((len_tokens_prompt + len_tokens_text) / 1000) * prices[model_name]['input_cost']
        output_cost = (max_tokens / 1000) * prices[model_name]['output_cost']
        return (len_tokens_prompt + len_tokens_text, input_cost + output_cost)

if __name__ == '__main__':
    # Configuramos los argumentos del programa
    parser = argparse.ArgumentParser(description="Esta herramienta realiza busquedas en los ficheros de un directorio")
    parser.add_argument('dir_path', type=str, help='La ruta al directorio donde se encuntran los ficheros')
    parser.add_argument('-r', '--regex', type=str, help='La expresion regular para realizar la busqueda.')
    parser.add_argument('-p', '--prompt', type=str, help='El prompt para realizar la busqueda con GPT.')
    parser.add_argument('-m', '--model', type=str, default='gpt-3.5-turbo-0125', help='El nombre del model de OpenAI para realizar la busqueda')
    parser.add_argument('--max-tokens', type=int, default=100, help='El numero maximo de tokens en la prediccion/generacion')

    # Paseamos los argumentos
    args = parser.parse_args()

    if args.regex:
        searcher = SmartSearch(args.dir_path)
        results = searcher.regex_search(args.regex)
        print()
        for file, res in results.items():
            print(file)
            for r in res:
                print(f'\t- {r}')


    if args.prompt:
        searcher = SmartSearch(args.dir_path)
        results = searcher.ia_search(args.prompt, args.model, args.max_tokens)
        print()
        for file, res in results.items():
            print(file)
            for r in res:
                print(f'\t- {r}')
