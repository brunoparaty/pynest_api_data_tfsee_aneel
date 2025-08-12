from nest.core import Module  
from src.modules.aneel.aneel_module import AneelModule
from src.app_controller import AppController 
from src.app_service import AppService   

@Module(
    imports=[AneelModule],
    controllers=[AppController], 
    providers=[AppService]  
)
class AppModule:
    pass