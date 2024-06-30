from playwright.sync_api import Page, expect
from locators.Locators import LocatorsPage
from settings import *

class GetValuesPage():
    def __init__(self, page: Page):
        self.page = page
        self.locators = LocatorsPage()

    def get_hrefs(self) -> Dict[str, Any]:
        """
            Coleta todos os atributos 'href' de elementos de uma página web.

            Este método utiliza um seletor para encontrar todos os elementos na página que correspondem a um localizador 
            de classe específico para hrefs. Os atributos 'href' desses elementos são coletados e retornados em uma lista.

            Returns:
                Dict[str, Any]: Um dicionário contendo os seguintes campos:
                    - "error" (bool): Indica se ocorreu algum erro durante a execução.
                    - "message" (str or None): Mensagem de erro, se houver.
                    - "data" (List[str]): Lista de atributos 'href' coletados da página.
        """
        try:
            list_hrefs = []

            elements = self.page.query_selector_all(self.locators.class_hrefs_page)
            for element in elements:
                
                list_hrefs.append(element.get_attribute('href'))
            
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            return {"error": True, "message": f"Error: {str(e)}", "data": None}
        
        return {"error": False, "message": None, "data": list_hrefs}
    
    def get_product_title(self) -> Dict[str, Any]:
        """
            Coleta títulos de produtos de uma página web, classificando-os conforme a presença de palavras específicas.

            Este método utiliza um seletor para encontrar todos os elementos na página que correspondem a um localizador 
            de classe específico para títulos de produtos. Os títulos são coletados, e aqueles que contêm "Serie" ou "Series" 
            são classificados como "V", enquanto os demais são classificados como "N".

            Returns:
                Dict[str, Any]: Um dicionário contendo os seguintes campos:
                    - "error" (bool): Indica se ocorreu algum erro durante a execução.
                    - "message" (str or None): Mensagem de erro, se houver.
                    - "data" (List[Dict[str, str]]): Lista de dicionários com os títulos dos produtos, onde a chave "N" indica títulos 
                    que não contêm "Serie" ou "Series", e a chave "V" indica títulos que contêm essas palavras.
        """
        try:
            all_title = self.page.query_selector_all(self.locators.class_pruduct_title)

            result_titles = []

            for title in all_title:
                text = title.text_content().strip()

                if "Serie" not in text and "Series" not in text:
                    result_titles.append({"N": text})

                else:
                    result_titles.append({"V": text})

        except Exception as e:
            logger.error(f"Error: {str(e)}")
            return {"error": True, "message": f"Error: {str(e)}", "data": None}
        
        return {"error": False, "message": None, "data": result_titles}

    def get_values_page(self) -> Dict[str, Any]:
        """
            Coleta valores monetários de uma página web.

            Este método utiliza um seletor para encontrar todos os elementos na página que correspondem a um localizador 
            de classe específico para valores monetários. Os valores são extraídos e retornados em uma lista.

            Returns:
                Dict[str, Any]: Um dicionário contendo os seguintes campos:
                    - "error" (bool): Indica se ocorreu algum erro durante a execução.
                    - "message" (str or None): Mensagem de erro, se houver.
                    - "data" (List[str]): Lista de valores monetários coletados da página.
        """
        try:
            values = self.page.query_selector_all(self.locators.class_money_page)
            all_values = []
            for value in values:

                all_values.append(value.inner_text())

        except Exception as e:
            logger.error(f"Error: {str(e)}")
            return {"error": True, "message": f"Error: {str(e)}", "data": None}
        
        return {"error": False, "message": None, "data": all_values}

    def scrolling_page(self) -> Dict[str, Any]:
        """
            Realiza a rolagem de uma página web, coleta dados e navega pelas páginas seguintes.

            Este método executa um loop para rolar a página, coletando títulos de produtos, valores e descrições.
            Ele também navega para a próxima página utilizando um link identificado pelo título "Seguinte".
            O processo continua até que não haja mais páginas para navegar.

            Returns:
                Dict[str, Any]: Um dicionário contendo os seguintes campos:
                    - "error" (bool): Indica se ocorreu algum erro durante a execução.
                    - "message" (str or None): Mensagem de erro, se houver.
                    - "data_values" (List[Any]): Lista de valores coletados das páginas.
                    - "data_description" (List[Any]): Lista de descrições coletadas das páginas.
                    - "data_hrefs" (List[Any]): Lista de hrefs coletados das páginas.
        """
        try:
            all_hrefs = []
            all_values = []
            all_description = []

            while True:
                locator = self.page.get_by_title("Seguinte")
                href_value = locator.get_attribute("href")

                result = self.get_product_title()
                if result['error']:
                    return result
                
                all_description.extend(result['data'])

                page_result = self.get_values_page()
                if page_result['error']:
                    return page_result

                all_values.extend(page_result['data'])

                get_href = self.get_hrefs()
                if get_href['error']:
                    return get_href
                
                all_hrefs.extend(get_href['data'])

                if href_value:
                    self.page.goto(href_value)
                    msg.info(f"O href contém o valor: {href_value}")
                else:
                    msg.info("O href está vazio")
                    break  

        except Exception as e:
            logger.error(f"Error: {str(e)}")
            return {"error": True, "message": f"Error: {str(e)}", "data": None}

        return {"error": False, "message": None, "data_values": all_values, "data_description": all_description, "data_hrefs": all_hrefs}