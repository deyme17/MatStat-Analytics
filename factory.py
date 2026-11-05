from utils import EventBus, AppContext
from services import UIMessager, DataVersionManager
from factories import (
    ControllersFactory, Controllers, UIFactory, ConnectFactory
)


class Factory:
    def __init__(self, window, context: AppContext):
        self.window = window
        self.context = context
        self.controllers: Controllers | None = None

    @classmethod
    def create(cls, window, context: AppContext) -> "Factory":
        factory = cls(window, context)
        factory._setup_context()
        factory._init_controllers()
        factory._setup_ui()
        factory._connect_ui()
        return factory

    def _setup_context(self) -> None:
        self.context.version_manager = DataVersionManager()
        self.context.messanger = UIMessager(parent=self.window)
        self.context.event_bus = EventBus()
        self.context.data_model = None

    def _init_controllers(self) -> None:
        self.controllers = ControllersFactory(self.window, self.context).create()

    def _setup_ui(self) -> None:
        UIFactory(self.window, self.context, self.controllers).setup_ui()

    def _connect_ui(self) -> None:
        ConnectFactory(self.window, self.context.event_bus, self.controllers).connect_ui()