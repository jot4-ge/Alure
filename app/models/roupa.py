from .produto import Produto

class Roupa(Produto):
    def __init__(self, id, nome, descricao, preco, estoque, image_url=None, tamanho=None):
        super().__init__(id, nome, descricao, preco, estoque, image_url)
        self.__tamanho = tamanho
    
    def _set_tamanho(self, tamanho):
        self.__tamanho = tamanho    
    
    def _get_tamanho(self):
        return self.__tamanho
        
    