from locators.Locators import LocatorsPage
from playwright.sync_api import Page
from utils.utils import new_module
from settings import *
import requests

class GetInfo():
    def __init__(self, page: Page):
        self.page = page
        self.locators = LocatorsPage()

    def get_value_price(self, values_produts, href_produts):
        """
            Coleta características e descrições de produtos de uma página web e cria um novo módulo com essas informações.

            Este método utiliza seletores para encontrar todos os elementos que contêm chaves de características e descrições 
            de produtos na página atual. Ele combina essas informações em um formato específico e as adiciona a uma lista de 
            características. Em seguida, ele cria um novo módulo com o valor do produto, as características e o href do produto.

            Args:
                values_produts (Any): Valor do produto a ser incluído no novo módulo.
                href_produts (str): Href da página do produto a ser incluído no novo módulo.

            Returns:
                Dict[str, Any]: Um dicionário contendo os seguintes campos:
                    - "error" (bool): Indica se ocorreu algum erro durante a execução.
                    - "message" (str or None): Mensagem de erro, se houver.
                    - "data" (None): Não retorna dados úteis além de um indicador de sucesso ou falha.
        """
        try:
            all_feature = []

            key_elements = self.page.query_selector_all(self.locators.class_key_caracter)
            value_elements = self.page.query_selector_all(self.locators.class_descricao_pruduct)

            for key, value in zip(key_elements, value_elements):
                chave_text = key.text_content().strip()
                value_text = value.text_content().strip()
                text = f'{chave_text}: {value_text}'
                all_feature.append(text)

            new_module(values_produts, all_feature, href_produts)

        except Exception as e:
            logger.error(f"Error: {str(e)}")
            return {"error": True, "message": f"Error: {str(e)}", "data": None}

        return {"error": False, "message": None, "data": None}

    def get_images(self, values_produts, href_produts):
        """
            Baixa imagens de produtos de uma página web e salva-as em um diretório local, em seguida, coleta o preço do produto.

            Este método utiliza um seletor para encontrar todos os elementos de imagem na página atual. Para cada imagem encontrada,
            ele baixa a imagem se o atributo 'src' estiver presente e a resposta do servidor for bem-sucedida (código de status 200).
            As imagens são salvas em um diretório específico. Após baixar as imagens, o método coleta o preço do produto.

            Args:
                values_produts (Any): Valor do produto que será passado para o método de coleta de preço.
                href_produts (str): Href da página do produto que será passado para o método de coleta de preço.

            Returns:
                Dict[str, Any]: Um dicionário contendo os seguintes campos:
                    - "error" (bool): Indica se ocorreu algum erro durante a execução.
                    - "message" (str or None): Mensagem de erro, se houver.
                    - "data" (None): Não retorna dados úteis além de um indicador de sucesso ou falha.
        """
        try:

            images = self.page.query_selector_all(self.locators.class_images_page)

            for img in images:
                download_images = img.get_attribute('src')

                if download_images:
                    
                    response = requests.get(download_images)
                    if response.status_code == 200:

                        name_element = os.path.basename(download_images)
                        save_path = os.path.join(PATH_IMG, name_element)

                        with open(save_path, 'wb') as f:
                            f.write(response.content)
                    else:
                        return {'error': True,'message': f"Failed to download image: {response.status_code}", 'data': None}
                    
            self.get_value_price(values_produts, href_produts)
                    
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            return {"error": True, "message": f"Error: {str(e)}", "data": None}
        
        return {"error": False, "message": None, "data": None}

    def characteristics(self, list_hrefs, values_products):
        """
            Navega para páginas de produtos e coleta imagens dos produtos com base em seus valores e hrefs.

            Este método percorre a lista de produtos, usando o índice de cada produto para obter o href correspondente.
            Ele navega para a página do produto utilizando o href e coleta imagens dos produtos.

            Args:
                list_hrefs (List[str]): Lista de hrefs das páginas dos produtos.
                values_products (List[Dict[str, Any]]): Lista de produtos com seus valores e índices, onde cada produto é 
                                                        representado por um dicionário contendo 'index' e 'value'.

            Returns:
                Dict[str, Any]: Um dicionário contendo os seguintes campos:
                    - "error" (bool): Indica se ocorreu algum erro durante a execução.
                    - "message" (str or None): Mensagem de erro, se houver.
                    - "data" (None): Não retorna dados úteis além de um indicador de sucesso ou falha.
        """
        try:
            for products in values_products:
                index = products['index']
                href = list_hrefs[index]

                self.page.goto(href)

                self.get_images(products['value'], href)

        except Exception as e:
            logger.error(f"Error: {str(e)}")
            return {"error": True, "message": f"Error: {str(e)}", "data": None}

        return {"error": False, "message": None, "data": None}
