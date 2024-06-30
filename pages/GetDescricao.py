from playwright.sync_api import Page, expect
from locators.Locators import LocatorsPage
from operator import itemgetter
from settings import *

class GetClassification():
    def __init__(self, page: Page):
        self.page = page
        self.locators = LocatorsPage()

    def get_rank_pruduct(self, value_list, description_list):
        """
            Classifica produtos com base em valores e descrições, retornando os três produtos com os menores valores.

            Este método verifica se o comprimento da lista de valores é igual ao da lista de descrições. Se forem iguais, ele
            percorre a lista de descrições para encontrar aqueles que contêm a chave 'V', coletando a descrição correspondente,
            o valor e o índice. Os resultados são classificados pelo valor em ordem crescente e os três menores valores são retornados.
            Em caso de discrepância no tamanho das listas, um erro é retornado.

            Args:
                value_list (List[Any]): Lista de valores dos produtos.
                description_list (List[Dict[str, str]]): Lista de descrições dos produtos, onde cada descrição é um dicionário
                                                        contendo a chave 'V' ou 'N'.

            Returns:
                Dict[str, Any]: Um dicionário contendo os seguintes campos:
                    - "error" (bool): Indica se ocorreu algum erro durante a execução.
                    - "message" (str or None): Mensagem de erro, se houver.
                    - "data" (List[Dict[str, Any]]): Lista dos três produtos com os menores valores, onde cada produto é representado 
                                                    por um dicionário contendo 'description', 'value' e 'index'.
        """
        try:
            if len(value_list) == len(description_list):
                results = []
                for i, description in enumerate(description_list):
                    if 'V' in description:
                        index = i
                        desc = description['V']
                        value = value_list[index]
                        results.append({"description": desc, "value": value, "index": index})
                
                sorted_results = sorted(results, key=itemgetter('value'))
                
                three_lowest = sorted_results[:3]
                
                return {"error": False, "message": None, "data": three_lowest}
            
            else:
                return {"error": True, "message": "Mismatch between the number of values and descriptions", "data": None}
        
        except Exception as e:
            return {"error": True, "message": f"Error: {str(e)}", "data": None}