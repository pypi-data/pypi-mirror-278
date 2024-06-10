import os

import requests

from maitai._config_listener_thread import ConfigListenerThread
from maitai_common.config import config_service
from maitai_gen.application import Application
from maitai_gen.config import Config as ActionConfig


class Config:
    maitai_host = os.environ.get("MAITAI_HOST", 'https://api.trymaitai.ai')
    maitai_ws = os.environ.get("MAITAI_WS", 'wss://humrvommw4.execute-api.us-west-2.amazonaws.com/production')

    def __init__(self):
        self._api_key = None
        self._applications: dict[str, Application] = {}
        self._company_id = None
        self.websocket_listener_thread = None
        self.config_listener_thread = None
        self._application_action_configs: dict[str, dict[str, ActionConfig]] = {}
        self.initialized = False

    @property
    def api_key(self):
        if self._api_key is None:
            if self.initialized:
                raise ValueError("Maitai API Key has not been set")
            else:
                self.initialize(api_key=os.environ.get("MAITAI_API_KEY"))
        return self._api_key

    @api_key.setter
    def api_key(self, value):
        self._api_key = value

    def initialize(self, api_key):
        self.api_key = api_key
        self._initialize_company()
        self.refresh_applications()
        self._initialize_websocket()
        self.initialized = True

    def get_application(self, application_ref_name: str) -> Application:
        return self._applications.get(application_ref_name)

    def get_application_action_config(self, application_ref_name: str, action_type: str) -> ActionConfig:
        return self._application_action_configs.get(application_ref_name, {}).get(action_type, config_service.get_default_config())

    def _initialize_company(self):
        host = self.maitai_host
        url = f'{host}/company/'
        headers = {
            'Content-Type': 'application/json',
            'x-api-key': self.api_key
        }

        response = requests.get(url, headers=headers, verify=False)
        self._company_id = response.json().get("id")

    def refresh_applications(self):
        host = self.maitai_host
        url = f'{host}/application/'
        headers = {
            'Content-Type': 'application/json',
            'x-api-key': self.api_key
        }

        response = requests.get(url, headers=headers, verify=False)
        applications = [Application().from_dict(app_json) for app_json in response.json()]
        for application in applications:
            self._applications[application.application_ref_name] = application
            for action_type in application.action_types:
                if application.application_ref_name not in self._application_action_configs:
                    self._application_action_configs[application.application_ref_name] = {}
                self._application_action_configs[application.application_ref_name][action_type.action_type] = action_type.meta

    def _initialize_websocket(self):
        self.config_listener_thread = ConfigListenerThread(self, self.maitai_ws, "APPLICATION_CONFIG_CHANGE", self._company_id)
        self.config_listener_thread.daemon = True
        self.config_listener_thread.start()


config = Config()
