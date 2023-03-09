import hashlib


# get the file bytes

file = open('britney.mp3', 'rb')
content = file.read()


m = hashlib.sha256()


# get the hash

m.update(content)

res = m.digest()

print(res)