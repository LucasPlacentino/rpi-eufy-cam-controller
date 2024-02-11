import json
import logging

class WSEufyApi:
    """https://bropat.github.io/eufy-security-ws/#/api_cmds"""
    #def __init__(self, websocket):
    #    self.websocket = websocket

    # ?? used
    driver_version: str
    server_version: str
    min_schema_version: float
    max_schema_version: float

    stations: list[str]
    devices: list[str]


    def handle_response(self, data: str, callback=None):
        parsed_data = json.loads(data)
        if "type" in parsed_data:
            if parsed_data["type"] == "version":
                self._handle_version(parsed_data)
            elif parsed_data["type"] == "result":
                self._handle_result(parsed_data)
            elif parsed_data["type"] == "event":
                self._handle_event(parsed_data)
            else:
                pass
        pass

    def _handle_version(self, parsed_data: dict):
        self.driver_version = parsed_data["driverVersion"]
        self.server_version = parsed_data["serverVersion"]
        self.min_schema_version = parsed_data["minSchemaVersion"]
        self.max_schema_version = parsed_data["maxSchemaVersion"]
        pass

    def _handle_result(self, parsed_data: dict):
        pass

    def _handle_event(self, parsed_data: dict):
        pass

    def send_command(self, websocket, command: str):
        pass

    def start_listening(self, websocket):
        pass

    #def set_api_schema(self, websocket, schema_version: int):
    #    websocket.send(json.dumps({"command": "set_api_schema", "messageId": 1, "version": schema_version}))

    def set2FAVerifyCode(self, websocket, messageId: str, code: str) -> bool:
        """compatible server schema version: 0+"""
        websocket.send(json.dumps({"command": "driver.set_verify_code", "messageId": messageId, "code": code}))

        data = websocket.recv()
        try:
            parsed_data = json.loads(data)
            if "result" in parsed_data:
                logging.debug("2FA_verify_code result response from server: ",parsed_data)
                return parsed_data["result"]
            else:
                logging.error("Invalid response from server after 2FA_verify_code message.")
                return False
        except json.JSONDecodeError as e:
            logging.error(e)
            #TODO: handle error
            return False
        
    def set_captcha(self, websocket, messageId: str, captchaId: str|None, captcha: str):
        """compatible server schema version: 7+"""
        pass

class Message:
    type: str
    id: str