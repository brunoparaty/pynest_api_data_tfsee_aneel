from nest.core import Controller, Get, Post, Depends
from src.modules.aneel.aneel_service import AneelService

@Controller('aneel-jobs')
class AneelController:
    
    def __init__(self, service: AneelService = Depends(AneelService)):
        self.service = service

    @Post("/pdf-generation/{termo_busca}")
    def iniciar_automacao_endpoint(self, termo_busca: str) -> dict:
        return self.service.iniciar_automacao(termo_busca)

    @Get("/{id_da_tarefa}")
    def obter_status_endpoint(self, id_da_tarefa: str) -> dict:
        return self.service.verificar_status(id_da_tarefa)
    
    @Get("/data-extraction/{termo_busca}")
    def obter_dados_boleto_sync_endpoint(self, termo_busca: str) -> dict:
        return self.service.obter_dados_boleto(termo_busca)