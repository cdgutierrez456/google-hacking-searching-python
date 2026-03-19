import os
import requests

class FileDownloader:
    def __init__(self, destination_directory):
        self.destination_directory = destination_directory
        self.create_directory()

    def create_directory(self):
        if not os.path.exists(self.destination_directory):
            os.makedirs(self.destination_directory)

    def file_download(self, url):
        try:
            respons = requests.get(url)
            file_name = url.split('/')[-1]
            complete_route = os.path.join(self.destination_directory, file_name)
            # Guardamos el documento en disco
            with open(complete_route, 'wb') as file:
                file.write(respons.content)
            print(f"Archivo {file_name} descargado en {complete_route}")
        except Exception as e:
            print(f"Error al descargar el archivo: {e}")

    def download_file_filter(self, urls, file_types=['all']):
        if file_types == ['all']:
            for url in urls:
                self.file_download(url)
        else:
            for url in urls:
                if any(url.endsWith(f'.{type}') for type in file_types):
                    self.file_download(url)