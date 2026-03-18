import json
from rich.console import Console
from rich.table import Table

class ResultsParser:

    def __init__(self, results):
        self.results = results

    def html_export(self, output_file):
        with open('html_template.html', 'r', encoding='utf-8') as f:
            template = f.read()

        html_elements = ''
        for index, result in enumerate(self.results, start=1):
            element = f'<div class="resultado">' \
                       f'<div class="indice">Resultado {index}</div>' \
                       f'<h5>{result['title']}</h5>' \
                       f'<p>{result['description']}</p>' \
                       f'<a href="{result['link']}" target="_blank">{result['link']}</a>' \
                       f'</div>'
            html_elements += element
        html_report = template.replace('{{ resultados }}', html_elements)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_report)
        print(f'Resultado exportados a HTML. Fichero creado: {output_file}')


    def json_export(self, output_file):
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=4)
        print(f'Resultado exportados a JSON. Fichero creado: {output_file}')

    def screen_show(self):
        console = Console()
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column('#', style='dim')
        table.add_column('Titulo', width=50)
        table.add_column('Descripcion')
        table.add_column('Enlace')

        for index, result in enumerate(self.results, start=1):
            table.add_row(str(index), result['title'], result['description'], result['link'])
            table.add_row('', '', '', '')

        console.print(table)