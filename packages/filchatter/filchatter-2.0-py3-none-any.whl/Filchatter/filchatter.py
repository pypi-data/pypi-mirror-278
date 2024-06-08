import requests

class Filchatter:
    url = "https://port-0-filchatter-1fgm12klx5u6yb5.sel5.cloudtype.app"

    def __init__(self, api_key= None):
        self.session = requests.Session()
        self.set_api_key(api_key)
        
    def set_api_key(self, key):
        self.api_key = key

    def get_api_key(self, name):
        target_url = self.url + "/api/generate_key_post"
        response = self.session.post(target_url, json={'name': name})
        return response
        
    # JSON 데이터를 보내는 POST 요청
    def send_json_request(self, chat, option = 1):
        target_url = self.url +"/api/receive_json"
        if self.api_key == None:
            print("You should set api key with set_api_key() method.")
            return
        elif chat == None:
            print("Invalid request.")
            return
        # 서버의 IP 주소와 포트

        data = {"chat": chat, "api_key": self.api_key, "option": option}
        response = self.session.post(target_url, json=data)
        return response