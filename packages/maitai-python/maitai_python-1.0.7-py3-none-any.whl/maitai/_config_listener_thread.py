import json

from maitai_common.processes.websocket_listener_thread import WebsocketListenerThread


class ConfigListenerThread(WebsocketListenerThread):
    def __init__(self, config, path, type, key=None):
        super(ConfigListenerThread, self).__init__(path, type, key)
        self.config = config

    def on_message(self, ws, message):
        event = json.loads(message)
        if event.get("event_type") == 'APPLICATION_CONFIG_CHANGE':
            self.config.refresh_applications()
