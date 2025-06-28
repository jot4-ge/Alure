from .produto import Produto

class Roupa(Produto):
    tamanho : str
    def __init__(self, id, nome, descricao, preco, estoque, image_filename, tamanho,categoria):
        super().__init__(id, nome, descricao, preco, estoque, image_filename, categoria)
        self.tamanho = tamanho
    
    def _set_tamanho(self, tamanho):
        self.tamanho = tamanho
    
    def _get_tamanho(self):
        return self.tamanho
    def to_dict(self):
        return {
            "id": self.id,  # Usa a property, que retorna o valor de _id
            "nome": self.nome,
            "preco": self.preco,  # Usa a property, que retorna o valor de _preco
            "estoque": self.estoque,  # Usa a property, que retorna o valor de _estoque
            "image_filename": self.image_filename,
            "categoria": self.categoria,
            "tamanho": self.tamanho
        }
        
    