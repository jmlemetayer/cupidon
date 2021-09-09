import json
import logging
import requests
import threading
import time

from urllib.parse import urljoin

logger = logging.getLogger("synology.auth")

class SynologyAuth():

    def __init__(self, parent):
        self.parent = parent
        self.session_id = None
        self.info = None

    def base_request(self, api, method, path, version, data=None):
        base_url = self.parent.settings.get("synology.url")
        api_url = urljoin(base_url, "webapi/")
        url = urljoin(api_url, path)

        if data is None:
            data = dict()
        data["api"] = api
        data["method"] = method
        data["version"] = version

        data_formatted = dict()
        for key, value in data.items():
            if isinstance(value, (list, tuple, bool)):
                data_formatted[key] = json.dumps(value)
            else:
                data_formatted[key] = value

        cookies = dict()
        if self.session_id is not None:
            cookies["id"] = self.session_id

        response = requests.post(url, data=data_formatted, cookies=cookies)

        assert response.ok
        assert response.json().get("success", False) == True
        return response.json().get("data")

    def get_info(self, query=None):
        if query is None:
            query = "all"
        data = dict()
        data["query"] = query
        return self.base_request("SYNO.API.Info", "query", "query.cgi", 1, data)

    def noauth_request(self, api, method, data=None):
        if self.info is None:
            self.info = self.get_info()

        info = self.info[api]

        return self.base_request(api, method, info["path"], info["maxVersion"], data)

    def login(self):
        data = dict()
        data["session"] = "DownloadStation"
        data["account"] = self.parent.settings.get("synology.username")
        data["passwd"] = self.parent.settings.get("synology.password")
        response = self.noauth_request("SYNO.API.Auth", "login", data)
        self.session_id = response["sid"]
        logger.info("Session is opened")

        def auto_logout():
            time.sleep(300)
            self.logout()

        thread = threading.Thread(target=auto_logout, daemon=True)
        thread.start()

    def logout(self):
        self.session_id = None
        data = dict()
        data["session"] = "DownloadStation"
        self.noauth_request("SYNO.API.Auth", "logout", data)
        logger.info("Session is closed")

    def request(self, api, method, data=None):
        if self.session_id is None:
            self.login()

        return self.noauth_request(api, method, data)
