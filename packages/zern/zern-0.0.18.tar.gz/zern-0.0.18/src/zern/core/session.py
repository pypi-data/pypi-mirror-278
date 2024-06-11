import requests
from time import sleep
import random
import pyotp

class Session:
    TYPE_GET = requests.get
    TYPE_POST = requests.post

    def __init__(self,user_name, password, totp_key) -> None:
        self.user_name = user_name
        self._private__password = password
        self.totp_key = totp_key
        self.cookies = None
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'accept-language': 'en-GB,en;q=0.8',
            'cache-control': 'max-age=0',
            'if-modified-since': 'Thu, 17 Oct 2019 07:18:26 GMT',
            'if-none-match': '"3147526947+gzip"',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        }
        self._base_url = 'https://kite.zerodha.com'
        self._login_url = 'https://kite.zerodha.com/api/login'
        self._totp_url = 'https://kite.zerodha.com/api/twofa'
        self._enc_token = None
        self.start()
        self._get_instruments()

    
    def start(self):
        resp = requests.get(self._base_url,headers=self.headers)
        self.cookies = resp.cookies
        sleep(random.random())
        print('login: waiting for almost 5 seconds')
        login_data = {'user_id': self.user_name,'password': self._private__password}
        resp = requests.post(self._login_url, cookies=self.cookies, headers=self.headers, data=login_data)
        if resp.status_code == 200:
            request_id = resp.json()['data']['request_id']
        else:
            try:
                obj = resp.json()
            except:
                raise Exception(f'error status {resp.status_code}: issue in the authentication code')
            raise Exception('{}: {}'.format(obj['status'],obj['message']))
        sleep(random.random())
        print('auto TOTP: waiting for almost 5 seconds')
        totp_data = {'user_id': self.user_name,'request_id': request_id,'twofa_value': pyotp.TOTP(self.totp_key).now(),'twofa_type': 'totp','skip_session': ''}
        response = requests.post('https://kite.zerodha.com/api/twofa', cookies=self.cookies, headers=self.headers, data=totp_data)
        self.cookies = response.cookies
        self._enc_token = self.cookies.get("enctoken")
        self.headers['authorization'] = 'enctoken {}'.format(self._enc_token)

        sleep(random.random())
        done = True
        try:
            success = response.json()['status']
        except:
            done = False
        if done:
            print('Authentication: {}'.format(success))
        else:
            print('Authentication: failed')
    
    def request(self,url,method=TYPE_GET,cookies=True,headers=True,data=None,params=None):
        response = method(url,
                          cookies=self.cookies if cookies else None,
                          headers=self.headers if headers else None,
                          data = data,
                          params=params)
        return response.json()

    def _get_instruments(self):
        new_headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-GB,en;q=0.9',
            'kite-iframe': 'kite_iframe_user',
            'origin': 'https://insights.sensibull.com',
            'referer': 'https://insights.sensibull.com/',
            'sec-ch-ua': '"Brave";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'sec-gpc': '1',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        }
        response = requests.get('https://oxide.sensibull.com/v1/compute/cache/insights/instrument_metacache/1', headers=new_headers)
        next_resp = requests.get('https://oxide.sensibull.com/v1/compute/cache/insights/underlying_instruments', headers=new_headers)
        print('getting instrument tokens')
        if response.status_code == 200:
            resp = response.json()
            del resp['etag']
            self.instruments = resp
            self.ins_details_cache = next_resp.json()['data']
        else:
            raise Exception('Failed to get instruments')
        
        #sleep(2)
        