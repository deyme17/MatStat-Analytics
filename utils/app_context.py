from models import DataModel
from .event_bus import EventBus
from services import DataVersionManager, UIMessager

class AppContext:
    def __init__(self):
        self.data_model: DataModel = None
        self.version_manager: DataVersionManager = None
        self.messanger: UIMessager = None
        self.event_bus: EventBus = None