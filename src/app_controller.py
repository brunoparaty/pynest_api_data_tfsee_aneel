from nest.core import Controller, Get, Depends
from src.app_service import AppService

@Controller('/')
class AppController:
    
    def __init__(self, service: AppService = Depends(AppService)):
        self.service = service

    @Get() # Endpoint: GET http://localhost:8000/
    def get_health(self) -> dict:
        """
        Endpoint para verificar a "saúde" da API.
        """
        return self.service.get_status()