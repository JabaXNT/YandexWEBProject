from requests import get, post


c = get('http://127.0.0.1:5000/users/1').json()
print(c)
