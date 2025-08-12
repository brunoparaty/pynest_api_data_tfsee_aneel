from nest.core import Module
from src.modules.aneel.aneel_controller import AneelController 
from src.modules.aneel.aneel_service import AneelService
@Module(
    controllers=[AneelController], 
    providers=[AneelService],
    exports=[AneelService]
)
class AneelModule:
    pass