import requests

class GoogleSearch:
    def __init__(self, api_key):
        """__init__

        Inicializa una nueva instancia de GoogleSearch
        Permite realizar peticiones automatizadas a la Api de serpapi
        Args:
            api_key (str): Clave api de google
        """
        self.api_key = api_key

    def search(self, query, start_page = 1, pages = 1, lang = 'lang_es'):
        """Realiza una busqueda en Google utilizando su API"""
        final_results = []
        results_per_page = 10 # Google muestra por defecto 10 resultados por pagina
        for page in range(pages):
            # Calcula el resultado de comienzo de cada pagina
            start_index = (start_page - 1) * results_per_page + 1 + (page * results_per_page)
            url = f'https://serpapi.com/search?api_key={self.api_key}&engine=google&q={query}&start={start_index}&lr={lang}'
            response = requests.get(url)

            # Comprobamos si la respuesta es correcta
            if response.status_code == 200:
                data = response.json()
                results = data.get("organic_results", [])
                cresults = self.custom_resulta(results)
                final_results.extend(cresults)
            else:
                print(f'Error obtenido al consultar la pagina {page}: HTTP {response.status_code}')
                break # Rompemos la iteracion actual
        return final_results

    def custom_resulta(self, results):
        """Filtra los resultado de la consulta"""
        custom_results = []
        for r in results:
            cresult = {}
            cresult['title'] = r.get('title')
            cresult['description'] = r.get('snippet')
            cresult['link'] = r.get('link')
            custom_results.append(cresult)

        return custom_results