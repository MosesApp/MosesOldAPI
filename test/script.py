import base64

file = open('decode', encoding='utf-8')
content = file.read()

print(base64.b64decode(bytes(content, 'utf-8')))
