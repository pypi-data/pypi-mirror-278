class ChunkUploadError(Exception):
    def __init__(self, mensagem, status_code):
        self.mensagem = mensagem
        self.status_code = status_code
        super().__init__(mensagem)

    def __str__(self):
        return f'Erro: {self.mensagem}. Status Code: {self.status_code}'
